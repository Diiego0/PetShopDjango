from django import template

register = template.Library()

@register.filter
def calcular_precio_descuento(precio, descuento):
    resultado = precio - (precio * descuento / 100)
    resultado_redondeado = round(resultado)
    return resultado_redondeado

