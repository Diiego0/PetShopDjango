from django.db import models

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
    descuentoSubP = models.IntegerField(null=False, blank=False, verbose_name="Descuento subscriptor")
    descuentoSubO = models.IntegerField(null=False, blank=False, verbose_name="Descuento oferta")
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