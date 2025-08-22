# gestion_riesgos/models.py

from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

# Modelo para la jerarquía de Categorías, usando django-mptt
class CategoriaRiesgo(MPTTModel):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    # El campo 'parent' crea la estructura de árbol
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['nombre']

    def __str__(self):
        # Muestra la jerarquía en el admin y otras representaciones de texto
        return "".join(["--"] * self.get_level()) + " " + self.nombre

# Modelo para definir los niveles de Probabilidad (Ej: Raro, Posible, Frecuente)
class Probabilidad(models.Model):
    nivel = models.CharField(max_length=50, unique=True)
    valor = models.IntegerField(unique=True, help_text="Valor numérico (ej: 1 para Bajo, 5 para Alto)")
    descripcion = models.TextField()

    class Meta:
        ordering = ['valor']

    def __str__(self):
        return f"{self.nivel} ({self.valor})"

# Modelo para definir los niveles de Impacto (Ej: Insignificante, Moderado, Catastrófico)
class Impacto(models.Model):
    nivel = models.CharField(max_length=50, unique=True)
    valor = models.IntegerField(unique=True, help_text="Valor numérico (ej: 1 para Bajo, 5 para Alto)")
    descripcion = models.TextField()

    class Meta:
        ordering = ['valor']

    def __str__(self):
        return f"{self.nivel} ({self.valor})"

# El modelo principal que representa un Riesgo identificado
class Riesgo(models.Model):
    ESTADOS_RIESGO = (
        ('abierto', 'Abierto'),
        ('en_tratamiento', 'En Tratamiento'),
        ('cerrado', 'Cerrado'),
        ('mitigado', 'Mitigado'),
    )

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = TreeForeignKey(CategoriaRiesgo, on_delete=models.SET_NULL, null=True, blank=True)
    probabilidad = models.ForeignKey(Probabilidad, on_delete=models.PROTECT, help_text="Probabilidad de que el riesgo ocurra.")
    impacto = models.ForeignKey(Impacto, on_delete=models.PROTECT, help_text="Impacto o consecuencia si el riesgo ocurre.")
    propietario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='riesgos_propios')
    fecha_identificacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_RIESGO, default='abierto')

    @property
    def nivel_riesgo(self):
        """ Calcula el Nivel de Riesgo Inherente (Probabilidad * Impacto) """
        if self.probabilidad and self.impacto:
            return self.probabilidad.valor * self.impacto.valor
        return 0

    def __str__(self):
        return self.nombre

# Modelo para las acciones de tratamiento de un riesgo
class TratamientoRiesgo(models.Model):
    riesgo = models.ForeignKey(Riesgo, on_delete=models.CASCADE, related_name='tratamientos')
    descripcion = models.TextField(help_text="Acción específica para mitigar, transferir, aceptar o evitar el riesgo.")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tratamientos_responsable')
    fecha_limite = models.DateField()
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Tratamiento para: {self.riesgo.nombre}"
    

##peligro

class Peligro(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    riesgos_asociados = models.ManyToManyField(Riesgo, related_name='peligros', blank=True)

    def __str__(self):
        return self.nombre