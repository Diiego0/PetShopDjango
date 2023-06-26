from django.shortcuts import render, redirect, get_object_or_404
from core.forms import *
from core.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from datetime import date
# Create your views here.

def index(request):
    productos = Producto.objects.all().order_by('idProducto')
    data = []

    for producto in productos:
        bodega = Bodega.objects.filter(nombreProducto=producto).first()
        if bodega is not None:
            stock_disponible = bodega.stockProducto
        else:
            stock_disponible = 0

        producto_data = {
            "producto": producto,
            "stock_disponible": stock_disponible
        }

        data.append(producto_data)

    return render(request, "core/index.html", {"productos": data})

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
            id_producto = form.cleaned_data['nombreProducto'].idProducto

            try:
                # Validar si ya existe un producto con el mismo ID
                if Bodega.objects.filter(idProductoBode=id_producto).exists():
                    messages.error(request, "Ya existe un producto con el mismo ID")
                    return redirect('bodega')

                bodega = Bodega(
                    categoriaProductoBode=categoria,
                    nombreProducto=nombre,
                    stockProducto=stock,
                    idProductoBode=id_producto
                )
                bodega.save()

                messages.success(request, "El producto fue agregado correctamente a la bodega")
                return redirect('bodega')

            except Exception as e:
                messages.error(request, "Ocurrió un error al agregar el producto a la bodega: {}".format(str(e)))
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
    usuario = request.user
    perfil = Perfil.objects.get(usuario=usuario)

    boletas = Boleta.objects.filter(cliente=perfil)
    historial = []
    for boleta in boletas:
        boleta_historial = {
            'nro_boleta': boleta.nro_boleta,
            'fecha_venta': boleta.fecha_venta,
            'fecha_despacho': boleta.fecha_despacho,
            'fecha_entrega': boleta.fecha_entrega,
            'total_a_pagar': boleta.total_a_pagar,
            'estado': boleta.estado,
        }
        historial.append(boleta_historial)
    return render(request, 'core/miscompras.html', {
        'historial': historial
    })

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
    bodega = Bodega.objects.filter(nombreProducto=producto).first()
    
    if bodega is not None:
        stock_disponible = bodega.stockProducto
        productos_relacionados = Producto.objects.exclude(idProducto=id).filter(bodega__categoriaProductoBode=bodega.categoriaProductoBode).order_by('?')[:5]
    else:
        stock_disponible = 0
        productos_relacionados = Producto.objects.exclude(idProducto=id).order_by('?')[:5]
    
    data = {
        "producto": producto,
        "bodega": bodega,
        "stock_disponible": stock_disponible,
        "productos_relacionados": productos_relacionados
    }
    
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


@user_passes_test(lambda u: u.is_staff)
def ventas(request):
    historial = Boleta.objects.all().values(
        'nro_boleta',
        'cliente__usuario__first_name',
        'cliente__usuario__last_name',
        'fecha_venta',
        'fecha_despacho',
        'fecha_entrega',
        'cliente__subscrito',
        'total_a_pagar',
        'estado'
    )
    historial = [
        {
            'nro_boleta': b['nro_boleta'],
            'nom_cliente': f'{b["cliente__usuario__first_name"]} {b["cliente__usuario__last_name"]}',
            'fecha_venta': b['fecha_venta'],
            'fecha_despacho': b['fecha_despacho'],
            'fecha_entrega': b['fecha_entrega'],
            'subscrito': 'Sí' if b['cliente__subscrito'] else 'No',
            'total_a_pagar': b['total_a_pagar'],
            'estado': b['estado']
        }
        for b in historial
    ]
    return render(request, 'core/ventas.html', { 
        'historial': historial 
    })


def boleta(request, nro_boleta):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    detalle_boleta = DetalleBoleta.objects.filter(boleta=boleta)
    datos = { 
        'boleta': boleta, 
        'detalle_boleta': detalle_boleta 
    }
    return render(request, 'core/boleta.html', datos)

@user_passes_test(lambda u: u.is_staff)
def cambiar_estado_boleta(request, nro_boleta, estado):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    if estado == 'Anulado':
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    else:
        if estado == 'Vendido':
            boleta.fecha_venta = date.today()
            boleta.fecha_despacho = None
            boleta.fecha_entrega = None
        elif estado == 'Despachado':
            boleta.fecha_despacho = date.today()
            boleta.fecha_entrega = None
        elif estado == 'Entregado':
            if boleta.estado == 'Vendido':
                boleta.fecha_despacho = date.today()
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Despachado':
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Entregado':
                boleta.fecha_entrega = date.today()
    boleta.estado = estado
    boleta.save()
    return redirect(reverse('ventas'))