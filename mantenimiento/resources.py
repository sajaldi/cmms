# mantenimiento/resources.py

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Rutina, Tarea, Activo, Marca, Modelo, Sistema

# Recurso para el modelo Rutina (que es un árbol)

class SistemaResource(resources.ModelResource):
    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(Sistema, 'pk')) # Puedes usar 'nombre' 
   
    class Meta:
        model = Sistema
        fields = ('id', 'nombre', 'descripcion', 'parent',)
        export_order = ('id', 'nombre', 'descripcion', 'parent',)

class RutinaResource(resources.ModelResource):
    # Definimos un widget para el campo 'parent' para que pueda buscarlo por nombre o pk al importar
    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(Rutina, 'pk')) # Puedes usar 'nombre' o 'codigo_rutina' si son únicos

    class Meta:
        model = Rutina
        fields = ('id', 'nombre', 'codigo_rutina', 'descripcion', 'parent', 'frecuencia',)
        export_order = ('id', 'nombre', 'codigo_rutina', 'descripcion', 'parent', 'frecuencia',)


class ActivoResource(resources.ModelResource):
    # Widget para que la importación sepa cómo encontrar el activo padre (por su ID)
    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(Activo, 'pk'))

    class Meta:
        model = Activo
        fields = ('id', 'tipo_de_activo','nombre', 'descripcion', 'ubicacion', 'fecha_adquisicion', 'parent',)
        export_order = fields # Mantenemos el orden definido

# Recurso para el modelo Tarea
class TareaResource(resources.ModelResource):
    class Meta:
        model = Tarea
        fields = ('id', 'nombre', 'descripcion',)




# --- NUEVO: Recurso para el modelo Marca ---
class MarcaResource(resources.ModelResource):
    class Meta:
        model = Marca
        fields = ('id', 'nombre', 'descripcion',)

class ModeloResource(resources.ModelResource):
    # Usamos un widget para poder importar usando el nombre de la marca en lugar de su ID
    marca = fields.Field(
        column_name='marca',
        attribute='marca',
        widget=ForeignKeyWidget(Marca, 'nombre'))
        
    class Meta:
        model = Modelo
        fields = ('id', 'nombre', 'marca', 'descripcion',)