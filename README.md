# Sistema de Inventario y Ventas

Proyecto del taller de aplicaciones en internet. Flask-AppBuilder + MySQL.


## Reglas de negocio

- Una venta se compone de un cliente, una fecha y líneas de detalle (producto + cantidad).
- El precio unitario y el subtotal se calculan automáticamente con el precio de venta del producto.
- Cada línea descuenta el stock; al eliminar la línea o la venta, el stock se restituye.
- No se permite vender más que el stock disponible, productos desactivados, cantidades menores o iguales a 0, ni repetir un producto en la misma venta.
- No se pueden eliminar categorías, proveedores, productos o clientes con registros relacionados.
- Se avisa cuando un producto queda con stock igual o inferior a su mínimo.