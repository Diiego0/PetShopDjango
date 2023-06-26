from django import template

register = template.Library()

@register.filter
def calcular_precio_descuento(precio, descuento):
    resultado = precio - (precio * descuento / 100)
    resultado_redondeado = round(resultado)
    return resultado_redondeado

@register.filter
def formatear_fecha(value):
    if value == None:
        value = '--/--/----'
    else:
        value = value.strftime("%d/%m/%Y")
    return f'{value}'

@register.filter
def formatear_dinero(value):
    value = round(value)
    value = f'${value:,}'
    value = value.replace(',', '.')
    return value

@register.filter
def formatear_porcentaje(value):
    return f'{value}%'