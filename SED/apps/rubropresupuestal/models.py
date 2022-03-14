from django.db import models


class Rubropresupuestal(models.Model):
    codigo = models.CharField(max_length=50,unique=True)
    nombre = models.CharField(max_length=500,null=False)
    idpadre = models.BigIntegerField(null=True)

def __str__(self):
    return f'{self.codigo} {self.nombre} {self.idpadre}'

