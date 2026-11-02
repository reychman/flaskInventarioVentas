from datetime import datetime, timedelta

from flask import request
from flask_appbuilder import BaseView, expose, has_access
from sqlalchemy import extract, func

from . import appbuilder
from .extensions import db
from .models import Categoria, Cliente, DetalleVenta, Producto, Proveedor, Venta


def _fecha(texto):
    """Convierte 'AAAA-MM-DD' a datetime. Devuelve None si está vacío o es inválido."""
    try:
        return datetime.strptime(texto, "%Y-%m-%d")
    except (TypeError, ValueError):
        return None


def _entero(texto):
    try:
        return int(texto)
    except (TypeError, ValueError):
        return None


class ReportesView(BaseView):
    route_base = "/reportes"
    default_view = "ventas_mensuales"

    @expose("/ventas_mensuales/")
    @has_access
    def ventas_mensuales(self):
        desde = _fecha(request.args.get("desde"))
        hasta = _fecha(request.args.get("hasta"))
        cliente_id = _entero(request.args.get("cliente"))

        anio = extract("year", Venta.fecha)
        mes = extract("month", Venta.fecha)
        q = (db.session.query(anio, mes, func.count(Venta.id),
                                func.coalesce(func.sum(Venta.total), 0))
            .group_by(anio, mes).order_by(anio, mes))
        if desde:
            q = q.filter(Venta.fecha >= desde)
        if hasta:
            q = q.filter(Venta.fecha < hasta + timedelta(days=1))
        if cliente_id:
            q = q.filter(Venta.cliente_id == cliente_id)

        datos = {(int(a), int(m)): (int(n), float(t)) for a, m, n, t in q.all()}

        filas = []
        if datos:
            (a, m), (a_fin, m_fin) = min(datos), max(datos)
            while (a, m) <= (a_fin, m_fin):
                n, t = datos.get((a, m), (0, 0.0))
                filas.append({"mes": f"{a}-{m:02d}", "ventas": n, "total": t})
                a, m = (a + 1, 1) if m == 12 else (a, m + 1)

        total = sum(f["total"] for f in filas)
        n_ventas = sum(f["ventas"] for f in filas)
        return self.render_template(
            "reportes/ventas_mensuales.html",
            filas=filas, total=total, n_ventas=n_ventas,
            promedio=(total / n_ventas) if n_ventas else 0,
            clientes=db.session.query(Cliente).order_by(Cliente.nombre).all(),
            f_desde=request.args.get("desde", ""), f_hasta=request.args.get("hasta", ""),
            f_cliente=cliente_id,
        )

    @expose("/top_productos/")
    @has_access
    def top_productos(self):
        desde = _fecha(request.args.get("desde"))
        hasta = _fecha(request.args.get("hasta"))
        categoria_id = _entero(request.args.get("categoria"))

        unidades = func.sum(DetalleVenta.cantidad)
        q = (db.session.query(Producto.codigo, Producto.nombre, unidades,
                            func.sum(DetalleVenta.subtotal))
            .join(DetalleVenta, DetalleVenta.producto_id == Producto.id)
            .join(Venta, Venta.id == DetalleVenta.venta_id)
            .group_by(Producto.id, Producto.codigo, Producto.nombre)
            .order_by(unidades.desc(), Producto.nombre))
        if desde:
            q = q.filter(Venta.fecha >= desde)
        if hasta:
            q = q.filter(Venta.fecha < hasta + timedelta(days=1))
        if categoria_id:
            q = q.filter(Producto.categoria_id == categoria_id)

        filas = [{"codigo": c, "nombre": n, "unidades": int(u), "monto": float(m)}
                for c, n, u, m in q.limit(5).all()]
        return self.render_template(
            "reportes/top_productos.html", filas=filas,
            categorias=db.session.query(Categoria).order_by(Categoria.nombre).all(),
            f_desde=request.args.get("desde", ""), f_hasta=request.args.get("hasta", ""),
            f_categoria=categoria_id,
        )

    @expose("/inventario_critico/")
    @has_access
    def inventario_critico(self):
        umbral = _entero(request.args.get("umbral"))
        categoria_id = _entero(request.args.get("categoria"))
        proveedor_id = _entero(request.args.get("proveedor"))

        q = db.session.query(Producto).filter(Producto.activo.is_(True))
        if umbral is not None:
            q = q.filter(Producto.stock <= umbral)            # umbral manual
        else:
            q = q.filter(Producto.stock <= Producto.stock_minimo)  # el de cada producto
        if categoria_id:
            q = q.filter(Producto.categoria_id == categoria_id)
        if proveedor_id:
            q = q.filter(Producto.proveedor_id == proveedor_id)
        productos = q.order_by(Producto.stock.asc(), Producto.nombre).all()

        return self.render_template(
            "reportes/inventario_critico.html", productos=productos,
            categorias=db.session.query(Categoria).order_by(Categoria.nombre).all(),
            proveedores=db.session.query(Proveedor).order_by(Proveedor.nombre).all(),
            f_umbral=umbral, f_categoria=categoria_id, f_proveedor=proveedor_id,
        )


appbuilder.add_view_no_menu(ReportesView)
appbuilder.add_link("Ventas mensuales", href="/reportes/ventas_mensuales/",
                    icon="fa-line-chart", category="Reportes")
appbuilder.add_link("Productos más vendidos", href="/reportes/top_productos/",
                    icon="fa-bar-chart", category="Reportes")
appbuilder.add_link("Inventario crítico", href="/reportes/inventario_critico/",
                    icon="fa-exclamation-triangle", category="Reportes")