from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.personalplanta.models import Personalplanta
from apps.tercero.models import Tercero
from apps.tipocontrato.models import Tipocontrato

class Solicitudpresupuestalcabecera(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    observacion = models.CharField(max_length=5000,null=False)
    personalplantaidsolicitante = models.ForeignKey(Personalplanta, on_delete= models.RESTRICT,related_name="FK_personalplantaidsolicitante")
    personalplantaidsolicitado = models.ForeignKey(Personalplanta, on_delete= models.RESTRICT,related_name="FK_personalplantaidsolicitado")
    terceroid = models.ForeignKey(Tercero, on_delete= models.RESTRICT)
    tipocontratoid = models.ForeignKey(Tipocontrato, on_delete= models.RESTRICT)
    fechainiciocontrato = models.DateField(null=False)
    fechafincontrato = models.DateField(null=False)
    contratonumero = models.CharField(max_length=50,null=False)
    objeto = models.CharField(max_length=5000, null=False,default='')
    estado = models.CharField(max_length=50, null=False,default='Procesado')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_solicitudpresupuestalcabecera_institucioneducativaid_consecutivo_unique")
        ]

    def __str__(self):
        return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha}{self.observacion}{self.personalplantaidsolicitante}{self.personalplantaidsolicitado}{self.terceroid}{self.tipocontratoid}{self.fechainiciocontrato}{self.fechafincontrato}{self.contratonumero}{self.objeto}{self.estado} '