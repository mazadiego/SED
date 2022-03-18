from django.db import models

class Periodo(models.Model):
    codigo = models.BigIntegerField(unique=True)
    activo = models.BooleanField(null=False)
    

def __str__(self):
    return f'{self.codigo} {self.activo}'
