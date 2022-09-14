from pyexpat import model
from django.db import models
from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera
from apps.rubropresupuestal.models import Rubropresupuestal
from apps.fuenterecurso.models import Fuenterecurso
# Create your models here.

class Solicitudpresupuestaldetalle(models.Model):
    solicitudpresupuestalcabeceraid = models.ForeignKey(Solicitudpresupuestalcabecera,related_name='solicitudpresupuestaldetalle',on_delete=models.RESTRICT)
    rubropresupuestalid = models.ForeignKey(Rubropresupuestal,on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    fuenterecursoid = models.ForeignKey(Fuenterecurso, on_delete=models.RESTRICT,null=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['solicitudpresupuestalcabeceraid', 'fuenterecursoid','rubropresupuestalid'], name="UK_solicitudpresupuestalcabeceraid_fuenterecursoid_rubropresupuestalid_unique")
        ]

    def __str__(self):
        return f'{self.solicitudpresupuestalcabeceraid} {self.rubropresupuestalid} {self.valor} {self.fuenterecursoid}'