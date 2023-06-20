from django import forms
from django.forms import ModelForm, fields
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field

class ProductoForm(ModelForm):
    descuentoSubP = forms.IntegerField(initial=5, label='Descuento subscriptor')
    descuentoSubO = forms.IntegerField(initial=0, label='Descuento oferta')
    class Meta:
        model = Producto
        fields = ['idProducto', 'categoriaProducto', 'nombreProducto', 'descripcionProducto', 'precioProducto', 'descuentoSubP', 'descuentoSubO', 'imagenProducto']
    

class BodegaForm(forms.ModelForm):
    categoriaProducto = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Categoría producto', widget=forms.Select(attrs={'class': 'form-select'}))
    nombreProducto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Nombre producto', widget=forms.Select(attrs={'class': 'form-select'}))
    stockProducto = forms.IntegerField(label='Stock producto')

    class Meta:
        model = Bodega
        fields = ['categoriaProducto', 'nombreProducto', 'stockProducto']