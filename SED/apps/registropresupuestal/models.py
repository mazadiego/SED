from datetime import date
from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.tercero.models import Tercero
from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal
from apps.tipocontrato.models import Tipocontrato

class Registropresupuestal(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    terceroid = models.ForeignKey(Tercero, on_delete= models.RESTRICT)
    observacion = models.CharField(max_length=500,null=False)
    certificadodisponibilidadpresupuestalid = models.ForeignKey(Certificadodisponibilidadpresupuestal,on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    objeto = models.CharField(max_length=5000, null=False,default='')
    estado = models.CharField(max_length=50, null=False,default='Procesado')
    tipocontratoid  = models.ForeignKey(Tipocontrato,on_delete=models.RESTRICT,null=True)
    fechainiciocontrato = models.DateField(null=False,default=date.today)
    fechafincontrato = models.DateField(null=False,default=date.today)
    contratonumero = models.CharField(max_length=50,null=False,default='')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_RP_institucioneducativaid_consecutivo_unique")
        ]
    
    def __str__(self):
        return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha} {self.terceroid} {self.observacion} {self.certificadodisponibilidadpresupuestalid} {self.valor} {self.objeto} {self.estado} {self.tipocontratoid} {self.fechainiciocontrato} {self.fechafincontrato} {self.contratonumero}'