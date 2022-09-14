from pyexpat import model
from sys import maxsize
from django.db import models
from apps.modificacionproyeccionpresupuestalcabecera.models import Modificacionproyeccionpresupuestalcabecera
from apps.fuenterecurso.models import Fuenterecurso
from apps.rubropresupuestal.models import Rubropresupuestal


class Modificacionproyeccionpresupuestaldetalle(models.Model):
    modificacionproyeccionpresupuestalid = models.ForeignKey(Modificacionproyeccionpresupuestalcabecera, related_name='modificacionproyeccionpresupuestaldetalle',on_delete=models.RESTRICT)
    fuenterecursoid = models.ForeignKey(Fuenterecurso,on_delete=models.RESTRICT)
    rubropresupuestalid = models.ForeignKey(Rubropresupuestal,on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=18,decimal_places=6,null=False)
    
    

def __str__(self):
    return f'{self.modificacionproyeccionpresupuestalid} {self.fuenterecursoid} {self.rubropresupuestalid} {self.valor}'
