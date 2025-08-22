from django.db import models

# Create your models here.
class ListaDeImpresion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tamano_etiqueta = models.CharField(max_length=50, choices=[
        ('pequeno', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    ], default='mediano')


    def __str__(self):
        return self.nombre
    
class ItemDeLista(models.Model):
    lista = models.ForeignKey(ListaDeImpresion, on_delete=models.CASCADE, related_name='items')
    nombre = models.CharField(max_length=100)
    campo_adicional = models.CharField(max_length=100, blank=True, null=True, help_text="Campo adicional opcional para personalizar la etiqueta.")
    # Este campo permite definir cuántas etiquetas se imprimirán para este ítem
    cantidad = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.nombre} (x{self.cantidad})"
