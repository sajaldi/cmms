from django.db import models

# Create your models here.
##Crear el modelo frecuencia

class Frecuencia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tiempo_entre_mantenimiento = models.PositiveIntegerField(help_text="Tiempo en días entre mantenimientos",null=True, blank=True)

    def __str__(self):
        return self.nombre