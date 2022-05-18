from django.db import models
from apps.tipoidentificacion.models import Tipoidentificacion

class Tercero(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=500,null=False)
    tipoidentificacionid = models.ForeignKey(Tipoidentificacion, on_delete=models.RESTRICT)   

def __str__(self):
    return f'{self.codigo} {self.nombre} {self.tipoidentificacionid}'
