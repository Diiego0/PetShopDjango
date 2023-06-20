from django import template

register = template.Library()

@register.filter
def calcular_precio_descuento(precio, descuento):
    porcentaje = 1 + (descuento / 100)
    resultado = precio * porcentaje
    resultado_redondeado = round(resultado)
    return resultado_redondeado