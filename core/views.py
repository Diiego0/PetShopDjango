from django.shortcuts import render, redirect, get_object_or_404
from core.forms import *
from core.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test, login_required
# Create your views here.

def index(request):
    data = {"list": Producto.objects.all().order_by('idProducto')}
    return render(request, "core/index.html", data)

def about(request):
    return render(request, "core/about.html")

@user_passes_test(lambda u: u.is_staff)
def administracion(request):
    return render(request, "core/administracion.html")

@user_passes_test(lambda u: u.is_staff)
def bodega(request):
    if request.method == "POST":
        form = BodegaForm(request.POST)
        if form.is_valid():
            categoria = form.cleaned_data['categoriaProducto']
            nombre = form.cleaned_data['nombreProducto']
            stock = form.cleaned_data['stockProducto']

            bodega = Bodega(
                categoriaProductoBode=categoria,
                nombreProductoBode=nombre,
                stockProducto=stock
            )
            bodega.save()
            
            messages.success(request, "El producto fue agregado correctamente a la bodega")
            return redirect('bodega')
    else:
        form = BodegaForm()
        
    lista_productos = Bodega.objects.all().order_by('idProductoBode')
    if request.method == "POST" and "eliminar" in request.POST:
        producto_id = request.POST.get('eliminar')
        producto = get_object_or_404(Bodega, idProductoBode=producto_id)
        producto.delete()
        messages.success(request, "El producto fue eliminado correctamente de la bodega")
        return redirect('bodega')
    
    return render(request, "core/bodega.html", {'form': form, 'lista_productos': lista_productos})

@login_required
def carrito(request):
    return render(request, "core/carrito.html")

@login_required
def miscompras(request):
    return render(request, "core/miscompras.html")

@user_passes_test(lambda u: u.is_staff)
def productos(request, action, id):
    data = {"form": ProductoForm, "action": action, "id": id}

    if action == 'ins':
        if request.method == "POST":
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    messages.success(request, "El producto fue ingresado correctamente")
                except:
                    messages.success(request, "No se pueden ingresar dos productos con el mismo ID")

    elif action == 'upd':
        objeto = Producto.objects.get(idProducto=id)
        if request.method == "POST":
            form = ProductoForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                messages.success(request, "El producto fue actualizado correctamente")
        data["form"] = ProductoForm(instance=objeto)

    elif action == 'del':
        try:
            Producto.objects.get(idProducto=id).delete()
            messages.success(request, "El producto fue eliminado correctamente")
            return redirect(productos, action='ins', id = '-1')
        except:
            messages.success(request, "El producto ya estaba eliminado")

    data["list"] = Producto.objects.all().order_by('idProducto')
    return render(request, "core/productos.html", data)


def ropa(request):
    return render(request, "core/ropa.html")

@user_passes_test(lambda u: u.is_staff)
def ventas(request):
    return render(request, "core/ventas.html")

@login_required
def misdatos(request):
    user = request.user
    perfil = user.perfil

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, "Datos actualizados correctamente")
            return redirect('misdatos')
    else:
        user_form = UserForm(instance=user)
        perfil_form = PerfilForm(instance=perfil)
    
    context = {
        'user': user,
        'perfil': perfil,
        'user_form': user_form,
        'perfil_form': perfil_form
    }
    
    return render(request, 'core/misdatos.html', context)


def ficha_producto(request, id):
    producto = Producto.objects.get(idProducto=id)
    data = {"producto":  producto}
    return render(request, "core/ficha.html", data)

def registro(request):

    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            subscrito = form.cleaned_data['subscrito']
            Perfil.objects.create(
                usuario=user, 
                tipo_usuario='Cliente', 
                rut=rut, 
                direccion=direccion, 
                subscrito=subscrito,
                imagen=request.FILES['imagen'])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect('index')
            
    return render(request, "registration/register.html", {'form': form})

@user_passes_test(lambda u: u.is_staff)
def usuarios(request, action, id):
    data = {"form": RegistroClienteForm, "action": action, "id": id}

    if action == 'ins':
        if request.method == "POST":
            form = RegistroClienteForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                rut = form.cleaned_data['rut']
                direccion = form.cleaned_data['direccion']
                subscrito = form.cleaned_data['subscrito']
                imagen = form.cleaned_data['imagen']
                perfil = Perfil(usuario=user, rut=rut, direccion=direccion, subscrito=subscrito, imagen=imagen)
                perfil.save()
                messages.success(request, "El usuario fue registrado correctamente")
                return redirect('usuarios', action='ins', id='-1')
        else:
            form = RegistroClienteForm()
        data["form"] = form

    elif action == 'upd':
        usuario = get_object_or_404(User, id=id)
        perfil = usuario.perfil
        if request.method == "POST":
            form = ActualizacionClienteForm(data=request.POST, files=request.FILES, instance=usuario)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                perfil.rut = form.cleaned_data['rut']
                perfil.direccion = form.cleaned_data['direccion']
                perfil.subscrito = form.cleaned_data['subscrito']
                if 'imagen' in request.FILES:
                    perfil.imagen = request.FILES['imagen']
                perfil.tipo_usuario = form.cleaned_data['tipo_usuario']  
                perfil.save()
                messages.success(request, "El usuario fue actualizado correctamente")
                return redirect('usuarios', action='ins', id='-1')
        else:
            form = ActualizacionClienteForm(instance=usuario, initial={
                'rut': perfil.rut,
                'direccion': perfil.direccion,
                'subscrito': perfil.subscrito,
                'imagen': perfil.imagen,
                'tipo_usuario': perfil.tipo_usuario  
            })
        data["form"] = form
        
    elif action == 'del':
        try:
            user = User.objects.get(id=id)
            user.delete()
            messages.success(request, "El usuario fue eliminado correctamente")
            return redirect(usuarios, action='ins', id='-1')
        except User.DoesNotExist:
            messages.success(request, "El usuario ya estaba eliminado")

    data["list"] = User.objects.filter(is_superuser=False).order_by('id')
    return render(request, "core/usuarios.html", data)