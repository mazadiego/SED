from pyexpat import model
from sys import maxsize
from django.db import models
from apps.periodo.models import Periodo
from apps.institucioneducativa.models import Institucioneducativa

class Modificacionproyeccionpresupuestalcabecera(models.Model):
    periodoid = models.ForeignKey(Periodo,on_delete=models.RESTRICT)
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    observacion = models.CharField(max_length=5000,blank=True)
    objeto = models.CharField(max_length=5000, null=False,default='')
    estado = models.CharField(max_length=50, null=False,default='Procesado')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['periodoid', 'institucioneducativaid'], name="UK_periodo_institucioneducativa_MPP_unique")
        ]

def __str__(self):
    return f'{self.periodoid} {self.institucioneducativaid} {self.observacion} {self.objeto}{self.estado}'