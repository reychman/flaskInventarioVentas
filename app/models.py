from datetime import datetime

from flask_appbuilder import Model
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        Numeric, String, Text)
from sqlalchemy.orm import relationship


class Categoria(Model):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(250), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    productos = relationship("Producto", back_populates="categoria")

    def __repr__(self):
        return self.nombre


class Proveedor(Model):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), unique=True, nullable=False)
    nit = Column(String(30), nullable=True)
    telefono = Column(String(30), nullable=True)
    email = Column(String(120), nullable=True)
    direccion = Column(String(200), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    productos = relationship("Producto", back_populates="proveedor")

    def __repr__(self):
        return self.nombre


class Cliente(Model):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False)
    ci_nit = Column(String(30), nullable=True)
    telefono = Column(String(30), nullable=True)
    email = Column(String(120), nullable=True)
    direccion = Column(String(200), nullable=True)

    ventas = relationship("Venta", back_populates="cliente")

    def __repr__(self):
        return self.nombre


class Producto(Model):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    codigo = Column(String(30), unique=True, nullable=False)
    nombre = Column(String(120), nullable=False)
    especificaciones = Column(Text, nullable=True)   # entrada para la IA (parte 3)
    descripcion = Column(Text, nullable=True)        # texto generado por la IA
    precio_compra = Column(Numeric(12, 2), default=0, nullable=False)
    precio_venta = Column(Numeric(12, 2), default=0, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    stock_minimo = Column(Integer, default=5, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    detalles = relationship("DetalleVenta", back_populates="producto")

    def __repr__(self):
        return self.nombre


class Venta(Model):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.now, nullable=False)
    total = Column(Numeric(12, 2), default=0, nullable=False)
    observacion = Column(String(250), nullable=True)

    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship(
        "DetalleVenta", back_populates="venta", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Venta #{self.id}"


class DetalleVenta(Model):
    __tablename__ = "detalle_ventas"
    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)

    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")

    def __repr__(self):
        return f"{self.cantidad} x {self.producto}"