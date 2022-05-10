from pyexpat import model
from django.db import models
from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera
from apps.rubropresupuestal.models import Rubropresupuestal
# Create your models here.

class Solicitudpresupuestaldetalle(models.Model):
    solicitudpresupuestalcabeceraid = models.ForeignKey(Solicitudpresupuestalcabecera,related_name='solicitudpresupuestaldetalle',on_delete=models.RESTRICT)
    rubropresupuestalid = models.ForeignKey(Rubropresupuestal,on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)

    def __str__(self):
        return f'{self.solicitudpresupuestalcabeceraid} {self.rubropresupuestalid} {self.valor}'