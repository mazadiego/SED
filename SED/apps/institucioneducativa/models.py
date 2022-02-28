from django.db import models
from apps.usuario.models import Usuario

class Institucioneducativa(models.Model):
    codigo = models.CharField(max_length=50,unique=True)
    nombre = models.CharField(max_length=500,null=False)
    usuarioid = models.ForeignKey(Usuario, on_delete=models.CASCADE)

def __str__(self):
    return f'{self.codigo} {self.nombre} {self.usuarioid}'
