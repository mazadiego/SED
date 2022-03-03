from django.db import models

from django.db import models
from apps.institucioneducativa.models import Institucioneducativa

class Personalplanta(models.Model):
    codigo = models.CharField(max_length=50,unique=True)
    nombre = models.CharField(max_length=500,null=False)
    cargo = models.CharField(max_length=500,null=False)
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)

def __str__(self):
    return f'{self.codigo} {self.nombre} {self.cargo} {self.institucioneducativaid}'

