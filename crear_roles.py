"""Crea el rol Vendedor y un usuario vendedor. Se ejecuta una sola vez:  python crear_roles.py"""
from getpass import getpass

from app import app, appbuilder

PERMISOS_VENDEDOR = [
    # Menús visibles
    ("menu_access", "Catálogo"), ("menu_access", "Productos"),
    ("menu_access", "Ventas"), ("menu_access", "Clientes"),
    # Productos: solo consultar (sin crear, editar, eliminar ni IA)
    ("can_list", "ProductoView"), ("can_show", "ProductoView"),
    # Clientes: consultar, crear y editar
    ("can_list", "ClienteView"), ("can_show", "ClienteView"),
    ("can_add", "ClienteView"), ("can_edit", "ClienteView"),
    # Ventas: consultar y crear (no editar ni eliminar ventas)
    ("can_list", "VentaView"), ("can_show", "VentaView"), ("can_add", "VentaView"),
    # Líneas de detalle: agregar y quitar
    ("can_list", "DetalleVentaInline"), ("can_show", "DetalleVentaInline"),
    ("can_add", "DetalleVentaInline"),
]

with app.app_context():
    sm = appbuilder.sm
    rol = sm.find_role("Vendedor") or sm.add_role("Vendedor")

    for permiso, vista in PERMISOS_VENDEDOR:
        pv = sm.find_permission_view_menu(permiso, vista)
        if pv is None:
            print(f"  ! No existe el permiso {permiso} en {vista} (¿arrancaste la app una vez?)")
            continue
        sm.add_permission_role(rol, pv)
    print("Rol Vendedor listo con", len(PERMISOS_VENDEDOR), "permisos.")

    if sm.find_user(username="vendedor1"):
        print("El usuario vendedor1 ya existe.")
    else:
        clave = getpass("Contraseña para el usuario vendedor1: ")
        sm.add_user("vendedor1", "Vendedor", "Demo", "vendedor1@correo.com", rol, clave)
        print("Usuario vendedor1 creado.")