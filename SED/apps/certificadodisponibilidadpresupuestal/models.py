from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera

# Create your models here.

class Certificadodisponibilidadpresupuestal(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    diasvalidez = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    observacion = models.CharField(max_length=500,null=True,blank=True)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    objeto = models.CharField(max_length=5000, null=False,default='')
    estado = models.CharField(max_length=50, null=False,default='Procesado')
    solicitudpresupuestalcabeceraid = models.ForeignKey(Solicitudpresupuestalcabecera,on_delete=models.RESTRICT, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_CDP_institucioneducativaid_consecutivo_unique")
        ]
    
    def __str__(self):
        return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha} {self.diasvalidez} {self.observacion} {self.valor} {self.objeto}{self.estado}{self.solicitudpresupuestalcabeceraid}'