from django import forms
from django.forms import ModelForm, fields, Form
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

form_hidden = {'class': 'd-none'}
form_select = {'class': 'form-select'}
form_control = {'class': 'form-control'}
form_text_area = {'class': 'form-control', 'rows': '3'}
form_file = {'class': 'form-control-file', 'title': 'Debe subir una imagen'}
form_check = {'class': 'form-check-input'}
form_password = {'class': 'form-control text-danger', 'value': '123'}

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



class RegistroClienteForm(UserCreationForm):
        
    rut = forms.CharField(
        max_length=15, 
        required=True, 
        label='RUT',
        widget=forms.TextInput(attrs=form_control),
    )
    direccion = forms.CharField(
        max_length=400, 
        required=True, 
        label='Dirección',
        widget=forms.Textarea(attrs=form_text_area),
    )
    subscrito = forms.BooleanField(
        required=False,
        label='Subscribirse',
        widget=forms.CheckboxInput(attrs=form_check),
    )
    imagen = forms.CharField(
        required=True,
        label='Imagen',
        widget=forms.FileInput(attrs=form_control),
    )
    
    
    class Meta:
        model = User
        fields = [
            'imagen', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'rut', 
            'direccion', 
            'password1', 
            'password2',
            'subscrito'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(form_control)
        self.fields['first_name'].widget.attrs.update(form_control)
        self.fields['last_name'].widget.attrs.update(form_control)
        self.fields['email'].widget.attrs.update(form_control)
        self.fields['password1'].widget.attrs.update(form_control)
        self.fields['password2'].widget.attrs.update(form_control)


class ActualizacionClienteForm(forms.ModelForm):
    rut = forms.CharField(
        max_length=15,
        required=True,
        label='RUT',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    direccion = forms.CharField(
        max_length=400,
        required=True,
        label='Dirección',
        widget=forms.Textarea(attrs=form_text_area),
    )
    subscrito = forms.BooleanField(
        required=False,
        label='Subscrito',
        widget=forms.CheckboxInput(attrs={'class': 'form-check'}),
    )
    imagen = forms.ImageField(
        required=False,  # Se cambia a False para que no sea obligatorio
        label='Imagen',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    is_staff = forms.BooleanField(label='Es staff', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    tipo_usuario = forms.ChoiceField(choices=Perfil.USUARIO_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'rut',
            'direccion',
            'subscrito',
            'imagen',
            'is_staff',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'rut', 'subscrito', 'direccion']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']