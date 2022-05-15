from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.rubropresupuestal.models import Rubropresupuestal
# Create your models here.

class Certificadodisponibilidadpresupuestal(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    diasvalidez = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    rubropresupuestalid = models.ForeignKey(Rubropresupuestal,on_delete=models.RESTRICT)
    observacion = models.CharField(max_length=500,null=False)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_CDP_institucioneducativaid_consecutivo_unique")
        ]
    
    def __str__(self):
        return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha} {self.diasvalidez} {self.rubropresupuestalid} {self.observacion} {self.valor}'