from django.db import models
from apps.ingresopresupuestal.models import Ingresopresupuestal
from apps.institucioneducativa.models import Institucioneducativa
from apps.tiporecaudo.models import Tiporecaudo

class Recaudopresupuestal(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    ingresopresupuestalid = models.ForeignKey(Ingresopresupuestal,on_delete=models.RESTRICT)
    tiporecaudoid = models.ForeignKey(Tiporecaudo,on_delete=models.RESTRICT)
    documentorecaudo= models.CharField(max_length=500,null=False)
    observacion = models.CharField(max_length=5000,blank=True)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_recaudopresupuestal_institucioneducativaid_consecutivo_unique")
        ]

    def __str__(self):
        return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha} {self.ingresopresupuestalid} {self.tiporecaudoid} {self.documentorecaudo} {self.observacion} {self.valor}'
