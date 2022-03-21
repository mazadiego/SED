from pyexpat import model
from sys import maxsize
from django.db import models
from apps.proyeccionpresupuestalcabecera.models import Proyeccionpresupuestalcabecera
from apps.fuenterecurso.models import Fuenterecurso
from apps.rubropresupuestal.models import Rubropresupuestal


class Proyeccionpresupuestaldetalle(models.Model):
    proyeccionpresupuestalid = models.ForeignKey(Proyeccionpresupuestalcabecera, related_name='proyeccionpresupuestaldetalle',on_delete=models.RESTRICT)
    fuenterecursoid = models.ForeignKey(Fuenterecurso,on_delete=models.RESTRICT)
    rubropresupuestalid = models.ForeignKey(Rubropresupuestal,on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    
    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['proyeccionpresupuestalid', 'fuenterecursoid','rubropresupuestalid'], name="UK_proyeccionpresupuestalid_fuenterecursoid_rubropresupuestalid_unique")
        ]

def __str__(self):
    return f'{self.proyeccionpresupuestalid} {self.fuenterecursoid} {self.rubropresupuestalid} {self.valor}'
