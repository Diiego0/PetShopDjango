from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
    
class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True, verbose_name="Id de categoría")
    nombreCategoria = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre de la categoría")

    def __str__(self):
        return self.nombreCategoria

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True, verbose_name="Id de producto")
    categoriaProducto = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name="Nombre de la categoría")
    nombreProducto = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre del producto")
    descripcionProducto = models.CharField(max_length=80, null=False, blank=False, verbose_name="Descripción del producto")
    precioProducto = models.IntegerField(null=False, blank=False, verbose_name="Precio del producto")
    descuentoSubP = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Descuento subscriptor")
    descuentoSubO = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Descuento oferta")
    imagenProducto = models.ImageField(upload_to="img/", default="sinfoto.jpg", null=False, blank=False, verbose_name="Imagen")

    def __str__(self):
        return self.nombreProducto

class Bodega(models.Model):
    idProductoBode = models.AutoField(primary_key=True, verbose_name="Id de producto")
    categoriaProductoBode = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name="Nombre de la categoría")
    nombreProductoBode = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre del producto")
    stockProducto = models.IntegerField(null=False, blank=False, verbose_name="Stock producto")

    def __str__(self):
        return self.nombreProductoBode

class Perfil(models.Model):
    USUARIO_CHOICES = [
        ('Cliente', 'Cliente'),
        ('Administrador', 'Administrador'),
        ('Superusuario', 'Superusuario'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(
        choices=USUARIO_CHOICES,
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Tipo de usuario'
    )
    rut = models.CharField(max_length=15, blank=False, null=False, verbose_name='RUT')
    direccion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Dirección')
    subscrito = models.BooleanField(blank=False, null=False, verbose_name='Subscrito')
    imagen = models.ImageField(upload_to='perfiles/', blank=False, null=False, verbose_name='Imagen')
    
    class Meta:
        db_table = 'Perfil'
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"
        ordering = ['tipo_usuario']

    def __str__(self):
        subscrito = ''
        if self.tipo_usuario == 'Cliente':
            subscrito = ' subscrito' if self.subscrito else ' no subscrito'
        return f'{self.usuario.first_name} {self.usuario.last_name} (ID {self.id} - {self.tipo_usuario}{subscrito})'
    

class Boleta(models.Model):
    ESTADO_CHOICES = [
        ('Anulado', 'Anulado'),
        ('Vendido', 'Vendido'),
        ('Despachado', 'Despachado'),
        ('Entregado', 'Entregado'),
    ]
    nro_boleta = models.IntegerField(primary_key=True, blank=False, null=False, verbose_name='Nro boleta')
    cliente = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    monto_sin_iva = models.IntegerField(blank=False, null=False, verbose_name='Monto sin IVA')
    iva = models.IntegerField(blank=False, null=False, verbose_name='IVA')
    total_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Total a pagar')
    fecha_venta = models.DateField(blank=False, null=False, verbose_name='Fecha de venta')
    fecha_despacho = models.DateField(blank=True, null=True, verbose_name='Fecha de despacho')
    fecha_entrega = models.DateField(blank=True, null=True, verbose_name='Fecha de entrega')
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=50, blank=False, null=False, verbose_name='Estado')
    
    class Meta:
        db_table = 'Boleta'
        verbose_name = "Boleta"
        verbose_name_plural = "Boletas"

    def __str__(self):
        return f'Boleta {self.nro_boleta} de {self.cliente.usuario.first_name} {self.cliente.usuario.last_name} por {formatear_dinero(self.total_a_pagar)}'

class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.DO_NOTHING)
    bodega = models.ForeignKey(Bodega, on_delete=models.DO_NOTHING)
    precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
    descuento_subscriptor = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto subs'
    )
    descuento_oferta = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto oferta'
    )
    descuento_total = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto total'
    )
    descuentos = models.IntegerField(blank=False, null=False, verbose_name='Descuentos')
    precio_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Precio a pagar')
    
    class Meta:
        db_table = 'DetalleBoleta'
        verbose_name = "Detalle de boleta"
        verbose_name_plural = "Detalles de boletas"

    def __str__(self):
        minimo_id = DetalleBoleta.objects.filter(boleta_id=self.boleta.nro_boleta).aggregate(minimo_id=Min('id'))['minimo_id']
        nro_item = self.id - minimo_id + 1
        return f'Boleta {self.boleta.nro_boleta} Item {nro_item} {self.bodega.producto.nombre} - {formatear_dinero(self.precio_a_pagar)}'
    
    def acciones():
        return {
            'accion_eliminar': 'eliminar el Detalle de la Boleta',
            'accion_actualizar': 'actualizar el Detalle de la Boleta'
        }
