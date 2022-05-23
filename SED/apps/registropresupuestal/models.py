from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.tercero.models import Tercero
from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal

class Registropresupuestal(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    terceroid = models.ForeignKey(Tercero, on_delete= models.RESTRICT)
    observacion = models.CharField(max_length=500,null=False)
    certificadodisponibilidadpresupuestalid = models.ForeignKey(Certificadodisponibilidadpresupuestal,on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_RP_institucioneducativaid_consecutivo_unique")
        ]
    
    def __str__(self):
        return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha} {self.terceroid} {self.observacion} {self.certificadodisponibilidadpresupuestalid} {self.valor}'