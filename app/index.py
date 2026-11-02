from datetime import datetime

from flask import redirect, url_for
from flask_appbuilder import expose
from flask_appbuilder.views import IndexView
from flask_login import current_user
from sqlalchemy import func

from .extensions import db
from .models import Cliente, Producto, Venta


class PanelIndexView(IndexView):
    """Página de inicio: panel con indicadores del negocio."""
    index_template = "panel.html"

    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for(self.appbuilder.sm.auth_view.endpoint + ".login"))
        self.update_redirect()
        ahora = datetime.now()
        inicio_mes = datetime(ahora.year, ahora.month, 1)

        ventas_mes, total_mes = db.session.query(
            func.count(Venta.id), func.coalesce(func.sum(Venta.total), 0)
        ).filter(Venta.fecha >= inicio_mes).one()

        productos_activos = db.session.query(func.count(Producto.id)).filter(
            Producto.activo.is_(True)).scalar()
        criticos = db.session.query(func.count(Producto.id)).filter(
            Producto.activo.is_(True), Producto.stock <= Producto.stock_minimo).scalar()
        clientes = db.session.query(func.count(Cliente.id)).scalar()

        ultimas = (db.session.query(Venta).order_by(Venta.fecha.desc()).limit(5).all())

        # El monto vendido solo lo ven quienes pueden abrir el reporte de ventas
        ver_montos = self.appbuilder.sm.has_access("can_ventas_mensuales", "ReportesView")

        return self.render_template(
            self.index_template,
            appbuilder=self.appbuilder,
            ventas_mes=ventas_mes, total_mes=total_mes, ver_montos=ver_montos,
            productos_activos=productos_activos, criticos=criticos,
            clientes=clientes, ultimas=ultimas, mes_actual=ahora.strftime("%m/%Y"),
        )