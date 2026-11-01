from datetime import datetime

from flask import flash, g, redirect, url_for
from flask_appbuilder import ModelView
from flask_appbuilder.actions import action
from flask_appbuilder.fieldwidgets import DateTimePickerWidget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms import DateTimeField
from wtforms.validators import Optional

from . import appbuilder
from .ai.asistente_ai import IAError, generar_descripcion
from .extensions import db
from .models import Categoria, Cliente, DetalleVenta, Producto, Proveedor, Venta

class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)
    list_title = "Categorías"
    label_columns = {"nombre": "Nombre", "descripcion": "Descripción",
                    "activo": "Activo", "productos": "Productos"}
    list_columns = ["nombre", "descripcion", "activo"]
    show_columns = ["id", "nombre", "descripcion", "activo", "productos"]
    add_columns = ["nombre", "descripcion", "activo"]
    edit_columns = add_columns
    search_columns = ["nombre", "activo"]
    order_columns = ["nombre"]

    def pre_delete(self, item):
        if item.productos:
            raise Exception("No se puede eliminar: la categoría tiene productos. "
                            "Puedes desactivarla en su lugar.")

class ProveedorView(ModelView):
    datamodel = SQLAInterface(Proveedor)
    list_title = "Proveedores"
    label_columns = {"nombre": "Nombre", "nit": "NIT", "telefono": "Teléfono",
                    "email": "Correo", "direccion": "Dirección",
                    "activo": "Activo", "productos": "Productos"}
    list_columns = ["nombre", "nit", "telefono", "email", "activo"]
    show_columns = ["id", "nombre", "nit", "telefono", "email", "direccion",
                    "activo", "productos"]
    add_columns = ["nombre", "nit", "telefono", "email", "direccion", "activo"]
    edit_columns = add_columns
    search_columns = ["nombre", "nit", "activo"]
    order_columns = ["nombre"]

    def pre_delete(self, item):
        if item.productos:
            raise Exception("No se puede eliminar: el proveedor tiene productos. "
                            "Puedes desactivarlo en su lugar.")

class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)
    list_title = "Clientes"
    label_columns = {"nombre": "Nombre", "ci_nit": "CI / NIT",
                    "telefono": "Teléfono", "email": "Correo",
                    "direccion": "Dirección", "ventas": "Ventas"}
    list_columns = ["nombre", "ci_nit", "telefono", "email"]
    show_columns = ["id", "nombre", "ci_nit", "telefono", "email",
                    "direccion", "ventas"]
    add_columns = ["nombre", "ci_nit", "telefono", "email", "direccion"]
    edit_columns = add_columns
    search_columns = ["nombre", "ci_nit"]
    order_columns = ["nombre"]

    def pre_delete(self, item):
        if item.ventas:
            raise Exception("No se puede eliminar: el cliente tiene ventas registradas.")

class ProductoView(ModelView):
    datamodel = SQLAInterface(Producto)
    list_title = "Productos"
    label_columns = {
        "codigo": "Código", "nombre": "Nombre",
        "especificaciones": "Especificaciones técnicas",
        "descripcion": "Descripción comercial",
        "precio_compra": "Precio de compra", "precio_venta": "Precio de venta",
        "stock": "Stock", "stock_minimo": "Stock mínimo", "activo": "Activo",
        "categoria": "Categoría", "proveedor": "Proveedor",
    }
    list_columns = ["codigo", "nombre", "categoria", "precio_venta",
                    "stock", "activo"]
    show_columns = ["id", "codigo", "nombre", "categoria", "proveedor",
                    "especificaciones", "descripcion", "precio_compra",
                    "precio_venta", "stock", "stock_minimo", "activo"]
    add_columns = ["codigo", "nombre", "categoria", "proveedor",
                    "especificaciones", "descripcion", "precio_compra",
                    "precio_venta", "stock", "stock_minimo", "activo"]
    edit_columns = add_columns
    search_columns = ["codigo", "nombre", "categoria", "proveedor", "activo"]
    order_columns = ["codigo", "nombre", "precio_venta", "stock"]

    def _validar(self, item):
        if item.stock is not None and item.stock < 0:
            raise Exception("El stock no puede ser negativo.")
        if item.precio_venta is not None and item.precio_venta < 0:
            raise Exception("El precio de venta no puede ser negativo.")
        if item.precio_compra is not None and item.precio_compra < 0:
            raise Exception("El precio de compra no puede ser negativo.")

    def pre_add(self, item):
        self._validar(item)

    def pre_update(self, item):
        self._validar(item)

    def pre_delete(self, item):
        if item.detalles:
            raise Exception("No se puede eliminar: el producto tiene ventas "
                            "registradas. Desactívalo en su lugar.")

    @action("generar_desc", "Generar descripción con IA",
            "¿Generar la descripción con IA? Se reemplazará la descripción actual.",
            "fa-magic", multiple=True, single=True)
    def generar_desc(self, items):
        if not isinstance(items, list):      # desde la ficha llega un solo producto
            items = [items]
        if len(items) > 10:
            flash("Selecciona máximo 10 productos a la vez.", "warning")
            return redirect(self.get_redirect())

        generados = 0
        for p in items:
            if not p.especificaciones or not p.especificaciones.strip():
                flash(f"'{p.nombre}': primero escribe sus especificaciones técnicas.",
                "warning")
                continue
            try:
                p.descripcion = generar_descripcion(
                    p.nombre, str(p.categoria), p.especificaciones)
                self.datamodel.edit(p)
                generados += 1
            except IAError as e:
                flash(f"'{p.nombre}': {e}", "danger")
                break                        # si falla la IA, no seguir intentando
        if generados:
            flash(f"Descripción generada para {generados} producto(s).", "success")
        self.update_redirect()
        return redirect(self.get_redirect())


class DetalleVentaInline(ModelView):
    """Líneas de detalle. Se usa dentro de la ficha de la venta."""
    datamodel = SQLAInterface(DetalleVenta)
    list_title = "Detalle de la venta"
    # Solo agregar y eliminar: para corregir una línea, se elimina y se vuelve a agregar
    base_permissions = ["can_add", "can_delete", "can_list", "can_show"]

    label_columns = {"producto": "Producto", "cantidad": "Cantidad",
                    "precio_unitario": "Precio unitario", "subtotal": "Subtotal"}
    list_columns = ["producto", "cantidad", "precio_unitario", "subtotal"]
    show_columns = ["venta", "producto", "cantidad", "precio_unitario", "subtotal"]
    add_columns = ["venta", "producto", "cantidad"]  # "venta" se oculta sola al abrirlo desde la ficha

    def pre_add(self, item):
        producto = item.producto
        venta = item.venta

        if producto is None:
            raise Exception("Debes seleccionar un producto.")
        if not item.cantidad or item.cantidad <= 0:
            raise Exception("La cantidad debe ser mayor a 0.")
        if not producto.activo:
            raise Exception(f"El producto '{producto.nombre}' está desactivado.")
        with db.session.no_autoflush:
            ya_esta = any(d is not item and d.producto_id == producto.id
                            for d in venta.detalles)
        if ya_esta:
            raise Exception(f"'{producto.nombre}' ya está en esta venta. Elimina "
                            "esa línea y vuelve a agregarla con la cantidad correcta.")
        if item.cantidad > producto.stock:
            raise Exception(f"Stock insuficiente de '{producto.nombre}': "
                            f"disponible {producto.stock}, solicitado {item.cantidad}.")

        # El precio y el subtotal los calcula el sistema, no el usuario
        item.precio_unitario = producto.precio_venta
        item.subtotal = producto.precio_venta * item.cantidad

        # Descuento de stock y actualización del total de la venta
        producto.stock -= item.cantidad
        venta.total = (venta.total or 0) + item.subtotal

    def post_add(self, item):
        p = item.producto
        if p.stock <= p.stock_minimo:
            flash(f"Atención: '{p.nombre}' quedó con stock bajo ({p.stock}).", "warning")

    def pre_delete(self, item):
        # Devuelve el stock y descuenta del total
        item.producto.stock += item.cantidad
        item.venta.total = (item.venta.total or 0) - item.subtotal


class VentaView(ModelView):
    datamodel = SQLAInterface(Venta)
    related_views = [DetalleVentaInline]
    list_title = "Ventas"
    show_title = "Venta"

    label_columns = {"fecha": "Fecha", "cliente": "Cliente", "total": "Total",
                    "observacion": "Observación", "detalles": "Detalle"}
    list_columns = ["id", "fecha", "cliente", "total"]
    show_columns = ["id", "fecha", "cliente", "total", "observacion"]
    add_columns = ["cliente", "fecha", "observacion"]
    edit_columns = ["cliente", "fecha", "observacion"]
    search_columns = ["fecha", "cliente", "total"]
    order_columns = ["id", "fecha", "total"]
    base_order = ("fecha", "desc")

    add_form_extra_fields = {
        "fecha": DateTimeField("Fecha (opcional: si la dejas vacía se usa ahora)",
                                validators=[Optional()],
                                widget=DateTimePickerWidget())
    }
    edit_form_extra_fields = add_form_extra_fields

    def pre_add(self, item):
        if not item.fecha:
            item.fecha = datetime.now()

    def pre_update(self, item):
        if not item.fecha:
            item.fecha = datetime.now()

    def post_add(self, item):
        g.nueva_venta_id = item.id
        flash("Venta creada. Ahora agrega los productos en la sección Detalle.", "info")

    def post_add_redirect(self):
        """Después de crear la venta, ir directo a su ficha para agregar líneas."""
        return redirect(url_for(self.endpoint + ".show", pk=g.nueva_venta_id))

    def pre_delete(self, item):
        # Al eliminar una venta, el stock de cada línea vuelve al producto
        for d in item.detalles:
            d.producto.stock += d.cantidad


appbuilder.add_view(CategoriaView, "Categorías", icon="fa-tags", category="Catálogo")
appbuilder.add_view(ProductoView, "Productos", icon="fa-cubes", category="Catálogo")
appbuilder.add_view(ProveedorView, "Proveedores", icon="fa-truck", category="Catálogo")
appbuilder.add_view(ClienteView, "Clientes", icon="fa-users", category="Ventas")
appbuilder.add_view(VentaView, "Ventas", icon="fa-shopping-cart", category="Ventas")
appbuilder.add_view_no_menu(DetalleVentaInline)