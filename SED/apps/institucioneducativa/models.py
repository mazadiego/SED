from django.db import models
from apps.user.models import User

class Institucioneducativa(models.Model):
    codigo = models.CharField(max_length=50,unique=True)
    nombre = models.CharField(max_length=500,null=False)
    usuarioid = models.ForeignKey(User, on_delete=models.RESTRICT,unique=True)

def __str__(self):
    return f'{self.codigo} {self.nombre} {self.usuarioid}'
