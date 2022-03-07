from django.db import models

class Tipoidentificacion(models.Model):
    codigo = models.CharField(max_length=50,unique=True)
    nombre = models.CharField(max_length=500,null=False)
    

def __str__(self):
    return f'{self.codigo} {self.nombre}'
