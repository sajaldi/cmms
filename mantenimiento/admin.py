# mantenimiento/admin.py

from django.contrib import admin

# --- Importaciones de Librerías ---
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

# --- Importaciones de tu Proyecto ---
from .models import Activo, Marca, Modelo, Rutina, PasoRutina, Tarea, PasosTarea, Sistema,Plano
from .resources import ActivoResource, RutinaResource, TareaResource, MarcaResource, ModeloResource, SistemaResource

# -----------------------------------------------------------------------------
# --- INLINES (Secciones anidadas) ---
# -----------------------------------------------------------------------------



class PasoRutinaInline(admin.TabularInline):
    model = PasoRutina
    extra = 1
    fields = ('orden', 'descripcion', 'duracion', 'es_paso_critico', 'peligro_asociado', 'medida_de_control')
    ordering = ('orden',)

class PasosTareaInline(admin.TabularInline):
    model = PasosTarea
    extra = 1

class ModeloInline(admin.TabularInline):
    model = Modelo
    extra = 1
    fields = ('nombre', 'descripcion')


class ActivoInline(admin.TabularInline):
    model = Activo
    extra = 1
    fields = ('nombre', 'tipo_de_activo', 'marca', 'modelo', 'parent', )

# -----------------------------------------------------------------------------
# --- CLASES DE ADMINISTRACIÓN (ADMINS) ---
# -----------------------------------------------------------------------------
##admin de Sistema 


###Inline de Sistema con respecto a su parent
class SistemaInline(admin.TabularInline):
    model = Sistema
    extra = 1
    fields = ('nombre',)


##admin de Planos
@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    inlines = [ActivoInline]
    search_fields = ('nombre',)
    

@admin.register(Sistema)
class SistemaAdmin(DraggableMPTTAdmin): # Herencia múltiple para árbol + import/export
    resource_class = SistemaResource
    inlines = [SistemaInline]
    list_display = (
        'tree_actions',
        'indented_title',
        'descripcion',
    )
    search_fields = ('nombre',)
    ordering = ('nombre',)  


@admin.register(Marca)
class MarcaAdmin(ImportExportModelAdmin): # Hereda solo de una clase para import/export
    resource_class = MarcaResource # Conectamos su recurso
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    inlines = [ModeloInline] # Mostramos los modelos dentro de la marca

@admin.register(Modelo)
class ModeloAdmin(ImportExportModelAdmin): # Hereda solo de una clase para import/export
    resource_class = ModeloResource # Conectamos su recurso
    inlines = [ActivoInline]
    list_display = ('nombre', 'marca')
    search_fields = ('nombre', 'marca__nombre')
    list_filter = ('marca',) # Permite filtrar modelos por marca

@admin.register(Activo)
class ActivoAdmin(ImportExportModelAdmin, DraggableMPTTAdmin): # Herencia múltiple para árbol + import/export
    """
    Clase de Admin para Activos.
    Combina la vista de árbol MPTT con la funcionalidad de import/export.
    """
    resource_class = ActivoResource
    list_display = (
        'tree_actions',
        'indented_title',
        'marca',
        'tipo_de_activo',
        'modelo',
        'ubicacion',
    )
    list_display_links = ('indented_title',)
    search_fields = ('nombre', 'descripcion', 'ubicacion', 'marca__nombre', 'modelo__nombre')
    
    # --- FILTROS AÑADIDOS ---
    # Esto creará una barra lateral de filtros en la página de lista de activos
    list_filter = (
        'tipo_de_activo', # Filtro por Tipo de Activo (desplegable)
        'marca',          # Filtro por Marca (desplegable)
        'parent',         # Filtro por Activo Padre (muy útil en jerarquías)
        'ubicacion',      # Filtro por Ubicación (si tienes ubicaciones comunes)
    )
    autocomplete_fields = ['parent', 'marca', 'modelo']

@admin.register(Rutina)
class RutinaAdmin(ImportExportModelAdmin, DraggableMPTTAdmin): # Herencia múltiple para árbol + import/export
    resource_class = RutinaResource
    list_display = (
        'tree_actions',
        'indented_title',
        'codigo_rutina',
        'frecuencia',
    )
    list_display_links = ('indented_title',)
    inlines = [PasoRutinaInline]
    search_fields = ('nombre', 'codigo_rutina')

@admin.register(Tarea)
class TareaAdmin(ImportExportModelAdmin): # Hereda solo de una clase para import/export
    resource_class = TareaResource
    list_display = ('nombre', 'descripcion')
    inlines = [PasosTareaInline]
    search_fields = ('nombre',)