from pyexpat import model
from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.registropresupuestal.models import Registropresupuestal

class Obligacionpresupuestal(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    recibosatisfacion = models.PositiveIntegerField(null=False)    
    registropresupuestalid = models.ForeignKey(Registropresupuestal,on_delete=models.RESTRICT)
    observacion = models.CharField(max_length=500,null=True,blank=True)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    objeto = models.CharField(max_length=5000, null=False,default='')
    estado = models.CharField(max_length=50, null=False,default='Procesado')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_OP_institucioneducativaid_consecutivo_unique")
        ]
    
    def __str__(self):
        return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha} {self.recibosatisfacion} {self.observacion} {self.registropresupuestalid} {self.valor} {self.objeto} {self.estado}'

