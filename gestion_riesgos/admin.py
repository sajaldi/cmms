# gestion_riesgos/admin.py

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import CategoriaRiesgo, Probabilidad, Impacto, Riesgo, TratamientoRiesgo, Peligro

# Usamos DraggableMPTTAdmin para una interfaz de arrastrar y soltar para las categorías
admin.site.register(
    CategoriaRiesgo,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)


#agrega Peligro al admin
@admin.register(Peligro)
class PeligroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)

    
# Admin simple para Probabilidad e Impacto
@admin.register(Probabilidad)
class ProbabilidadAdmin(admin.ModelAdmin):
    list_display = ('nivel', 'valor', 'descripcion')

@admin.register(Impacto)
class ImpactoAdmin(admin.ModelAdmin):
    list_display = ('nivel', 'valor', 'descripcion')

# Admin más completo para el modelo Riesgo
@admin.register(Riesgo)
class RiesgoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'probabilidad', 'impacto', 'nivel_riesgo', 'estado')
    list_filter = ('estado', 'categoria', 'probabilidad', 'impacto')
    search_fields = ('nombre', 'descripcion')

# Registrar el modelo de Tratamiento
admin.site.register(TratamientoRiesgo)

