# mantenimiento/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from gestion_riesgos.models import Riesgo
from core.models import Frecuencia 
# Si usas los modelos Activo y OrdenTrabajo en otras partes, debes mantenerlos importados.
# Si solo usas los modelos que me diste, usaremos solo esos.

# Asumo que NO USAS Activo y OrdenTrabajo en la lista, por lo que los elimino de este archivo.
# Si necesitas mantenerlos, por favor, inclúyemelos en la lista de modelos.

####Modelo Sistema #######

###Refactoriza como modelo MPTT para jerarquías

class Sistema(MPTTModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['nombre']

    def __str__(self):
        return f"{'--' * self.get_level()} {self.nombre}"
    

### clase modelo

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Modelo(models.Model):

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='modelos')
    Sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, related_name='modelos', null=True, blank=True)   

    def __str__(self):
        return f"{self.nombre} ({self.marca.nombre})"   
    

#### Clase Plano

class Plano(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    tipo_de_plano = models.CharField(max_length=50, choices=[
        ('proyecto_ejecutivo', 'Proyecto Ejecutivo'),
        ('asbuilt', 'Plano As Built'),
        
    ])
    no_de_documento = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.nombre


class Activo(MPTTModel):
    TIPO_ACTIVO_CHOICES = [
        ('ubicacion_funcional', 'Ubicación Funcional'),
        ('equipo', 'Equipo'),
        ('herramienta', 'Herramienta'),
        ('otro', 'Otro')
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='activos', null=True, blank=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name='activos', null=True, blank=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True, help_text="Ubicación física o descriptiva del activo.")
    fecha_adquisicion = models.DateField(blank=True, null=True)
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE, related_name='activos', null=True, blank=True)
    tipo_de_activo = models.CharField(
        max_length=50,  
        choices=TIPO_ACTIVO_CHOICES,
        default='otro',
        help_text="Tipo de activo."
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['nombre']

    # --- MÉTODO __str__ ACTUALIZADO ---
    # --- MÉTODO __str__ ALTERNATIVO PARA RUTA COMPLETA ---
    def __str__(self):
        # get_ancestors() nos da una lista de todos los padres. 'include_self=True' nos incluye en la lista.
        nombres = [nodo.nombre for nodo in self.get_ancestors(include_self=True)]
        # Unimos los nombres con un separador
        return " > ".join(nombres)
        


# --- MODELO RUTINA COMPLETO Y CORREGIDO ---
class Rutina(MPTTModel):
    nombre = models.CharField(max_length=100)
    codigo_rutina = models.CharField(max_length=50, unique=True, blank=True, null=True) # <-- ESTE CAMPO ESTABA FALTANDO
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True,null=True,blank=True)# <-- ESTE CAMPO ESTABA FALTANDO
    fecha_actualizacion = models.DateTimeField(auto_now=True) # <-- ESTE CAMPO ESTABA FALTANDO
    
    # MPTT Parent
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    frecuencia = models.ForeignKey(Frecuencia, on_delete=models.CASCADE, related_name='rutinas', null=True, blank=True)
    
    class MPTTMeta:
        order_insertion_by = ['nombre']

    def __str__(self):
        # Muestra la jerarquía en los selectores
        return f"{'--' * self.get_level()} {self.nombre}"

# --- MODELO PASORUTINA ---
class PasoRutina(models.Model):
    NIVEL_RIESGO_CHOICES = (
        ('ALTO', 'Alto'),
        ('MEDIO', 'Medio'),
        ('BAJO', 'Bajo'),
    )

    rutina = models.ForeignKey(Rutina, related_name='pasos', on_delete=models.CASCADE)
    descripcion = models.TextField()
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")
    orden = models.PositiveIntegerField()

    es_paso_critico = models.BooleanField(default=False, help_text="Marcar si este paso involucra un riesgo significativo de seguridad.")
    peligro_asociado = models.TextField(blank=True, null=True, help_text="Descripción del peligro específico (ej: Contacto eléctrico, Exposición química).")
    medida_de_control = models.TextField(blank=True, null=True, help_text="Equipo de protección personal requerido o acción para mitigar el peligro.")
    nivel_riesgo_paso = models.CharField(max_length=5, choices=NIVEL_RIESGO_CHOICES, blank=True, null=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.rutina.nombre} - Paso {self.orden}"

# --- MODELO TAREA ---
class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

# --- MODELO PASOSTAREA ---
class PasosTarea(models.Model):
    tarea = models.ForeignKey(Tarea, related_name='pasos', on_delete=models.CASCADE)
    descripcion = models.TextField()
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")
    orden = models.PositiveIntegerField()

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.tarea.nombre} - Paso {self.orden}"
    

