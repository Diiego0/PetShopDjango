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
    path('usuarios/<action>/<id>/', usuarios, name="usuarios"),
    path('ventas', ventas, name="ventas"),
    path('misdatos', misdatos, name="misdatos"),
    path('ficha_producto/<id>', ficha_producto, name="ficha_producto"),
    path('registro/', registro, name='registro'),
    path('boleta/<nro_boleta>', boleta, name='boleta'),
    path('cambiar_estado_boleta/<nro_boleta>/<estado>', cambiar_estado_boleta, name='cambiar_estado_boleta'),



]
