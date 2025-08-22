from django.contrib import admin

# Register your models here.
#Registrar Frecuencia
from .models import Frecuencia  
@admin.register(Frecuencia)
class FrecuenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

    