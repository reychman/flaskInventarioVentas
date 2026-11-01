from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder
from .models import Categoria, Cliente, Producto, Proveedor


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


appbuilder.add_view(CategoriaView, "Categorías", icon="fa-tags", category="Catálogo")
appbuilder.add_view(ProductoView, "Productos", icon="fa-cubes", category="Catálogo")
appbuilder.add_view(ProveedorView, "Proveedores", icon="fa-truck", category="Catálogo")
appbuilder.add_view(ClienteView, "Clientes", icon="fa-users", category="Ventas")