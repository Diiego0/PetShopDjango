from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .forms import ActualizacionClienteForm

# Register your models here.


admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Bodega)
admin.site.register(Perfil)
admin.site.register(Boleta)

class DetalleBoletaAdmin(admin.ModelAdmin):
    list_display = ('id', 'boleta', 'bodega', 'precio_a_pagar')
    # Agrega cualquier otra configuración que desees

admin.site.register(DetalleBoleta, DetalleBoletaAdmin)

class ActualizacionClienteFormAdmin(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        form = ActualizacionClienteForm


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False


class CustomUserAdmin(UserAdmin):
    form = ActualizacionClienteFormAdmin
    inlines = (PerfilInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)