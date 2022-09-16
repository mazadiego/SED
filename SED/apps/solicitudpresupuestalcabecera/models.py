from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.personalplanta.models import Personalplanta


class Solicitudpresupuestalcabecera(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    observacion = models.CharField(max_length=5000,null=True,blank=True)
    personalplantaidsolicitante = models.ForeignKey(Personalplanta, on_delete= models.RESTRICT,related_name="FK_personalplantaidsolicitante")
    personalplantaidsolicitado = models.ForeignKey(Personalplanta, on_delete= models.RESTRICT,related_name="FK_personalplantaidsolicitado")
    objeto = models.CharField(max_length=5000, null=False,default='')
    estado = models.CharField(max_length=50, null=False,default='Procesado')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_solicitudpresupuestalcabecera_institucioneducativaid_consecutivo_unique")
        ]

    def __str__(self):
        return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha}{self.observacion}{self.personalplantaidsolicitante}{self.personalplantaidsolicitado}{self.objeto}{self.estado} '