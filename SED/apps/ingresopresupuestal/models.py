from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.tercero.models import Tercero
from apps.fuenterecurso.models import Fuenterecurso

class Ingresopresupuestal(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)
    fecha = models.DateField(null=False)
    terceroid = models.ForeignKey(Tercero,on_delete=models.RESTRICT)
    fuenterecursoid = models.ForeignKey(Fuenterecurso,on_delete=models.RESTRICT)
    observacion = models.CharField(max_length=5000,blank=True)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    fechaproyeccionrecaudo = models.DateField(null=False)
    objeto = models.CharField(max_length=5000, null=False,default='')
    estado = models.CharField(max_length=50, null=False,default='Procesado')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','consecutivo'], name="UK_institucioneducativaid_consecutivo_unique")
        ]

def __str__(self):
    return f'{self.institucioneducativaid} {self.consecutivo} {self.fecha} {self.terceroid} {self.fuenterecursoid} {self.observacion} {self.valor} {self.fechaproyeccionrecaudo}{self.objeto}{self.estado} '