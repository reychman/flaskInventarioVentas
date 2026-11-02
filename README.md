# Sistema de Inventario y Ventas

Proyecto del taller de aplicaciones en internet. Flask-AppBuilder + MySQL.


## Reglas de negocio

- Una venta se compone de un cliente, una fecha y líneas de detalle (producto + cantidad).
- El precio unitario y el subtotal se calculan automáticamente con el precio de venta del producto.
- Cada línea descuenta el stock; al eliminar la línea o la venta, el stock se restituye.
- No se permite vender más que el stock disponible, productos desactivados, cantidades menores o iguales a 0, ni repetir un producto en la misma venta.
- No se pueden eliminar categorías, proveedores, productos o clientes con registros relacionados.
- Se avisa cuando un producto queda con stock igual o inferior a su mínimo.


## IA (Groq)

En Catálogo → Productos, la acción **Generar descripción con IA** redacta la descripción comercial a partir de las especificaciones técnicas, usando la API de Groq (modelo configurable con `GROQ_MODEL`). La clave va en `.env` como `GROQ_API_KEY`.

## Seguridad

- Inicio de sesión obligatorio en todas las vistas; sin registro público de usuarios.
- Rol **Admin**: acceso completo. Rol **Vendedor**: consulta productos, gestiona clientes y registra ventas; no puede modificar el catálogo, eliminar ventas ni usar la IA.
- Los roles se crean con `python crear_roles.py`. Sesión con expiración de 30 minutos y protección CSRF.


## Reportes

- **Ventas mensuales** (gráfico de líneas): total vendido por mes, con filtros por fechas y cliente.
- **Productos más vendidos** (gráfico de barras): top 5 por unidades, con filtros por fechas y categoría.
- **Inventario crítico** (listado): productos activos con stock menor o igual al umbral, con filtros por umbral, categoría y proveedor.

El panel de inicio resume ventas del mes, productos activos, productos críticos y clientes.

## Instalación

1. Crear la base de datos `inventario_ventas` en MySQL (Laragon).
2. `py -3.14 -m venv venv` y `venv\Scripts\activate.bat`
3. `python -m pip install -r requirements.txt`
4. `python init_db.py`
5. `flask --app run fab create-admin`
6. `python crear_roles.py`
7. `python run.py`