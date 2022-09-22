from django.db import models
from apps.institucioneducativa.models import Institucioneducativa

# Create your models here.

class Adjuntos(models.Model):
    tipodocumento = models.IntegerField(null=False)
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    nombrearchivo = models.CharField(max_length=500,null=False)
    archivobase64 = models.FileField(blank=False,null=False,upload_to='files/')

def __str__(self):
    return f'{self.tipodocumento} {self.institucioneducativaid} {self.consecutivo}{self.nombrearchivo}{self.archivobase64}'