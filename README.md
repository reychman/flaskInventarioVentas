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