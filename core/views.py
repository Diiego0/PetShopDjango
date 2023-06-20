from django.shortcuts import render, redirect, get_object_or_404
from core.forms import *
from core.models import *
from django.contrib import messages
# Create your views here.

def index(request):
    data = {"list": Producto.objects.all().order_by('idProducto')}
    return render(request, "core/index.html", data)

def about(request):
    return render(request, "core/about.html")

def administracion(request):
    return render(request, "core/administracion.html")

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

def carrito(request):
    return render(request, "core/carrito.html")

def miscompras(request):
    return render(request, "core/miscompras.html")

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

def register(request):
    return render(request, "core/register.html")

def usuarios(request):
    return render(request, "core/usuarios.html")

def ventas(request):
    return render(request, "core/ventas.html")

def misdatos(request):
    return render(request, "core/misdatos.html")

def ficha_producto(request, id):
    producto = Producto.objects.get(idProducto=id)
    data = {"producto":  producto}
    return render(request, "core/ficha.html", data)
