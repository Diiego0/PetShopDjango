from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name="index"),
    path('about', about, name="about"),
    path('administracion', administracion, name="administracion"),
    path('bodega', bodega, name="bodega"),
    path('carrito', carrito, name="carrito"),
    path('miscompras', miscompras, name="miscompras"),
    path('productos/<action>/<id>/', productos, name="productos"),
    path('ropa', ropa, name="ropa"),
    path('register', register, name="register"),
    path('usuarios', usuarios, name="usuarios"),
    path('ventas', ventas, name="ventas"),
    path('misdatos', misdatos, name="misdatos"),
    path('ficha_producto/<id>', ficha_producto, name="ficha_producto"),



]
