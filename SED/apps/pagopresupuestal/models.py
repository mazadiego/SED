from pyexpat import model
from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.obligacionpresupuestal.models import Obligacionpresupuestal

class Pagopresupuestal(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    obligacionpresupuestalid = models.ForeignKey(Obligacionpresupuestal,on_delete=models.RESTRICT)
    observacion = models.CharField(max_length=500,null=False)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    objeto = models.CharField(max_length=5000, null=False,default='')
    estado = models.CharField(max_length=50, null=False,default='Procesado')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_PagoPresu_institucioneducativaid_consecutivo_unique")
        ]
    
    def __str__(self):
        return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha} {self.observacion} {self.obligacionpresupuestalid} {self.valor} {self.objeto} {self.estado}'

