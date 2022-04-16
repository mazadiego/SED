from django.db import models

from apps.institucioneducativa.models import Institucioneducativa

class Consecutivo(models.Model):
    
    tipodocumento = models.IntegerField(null=False)
    institucioneducativaid = models.ForeignKey(Institucioneducativa, on_delete=models.RESTRICT)
    consecutivo = models.PositiveIntegerField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipodocumento', 'institucioneducativaid','consecutivo'], name="UK_tipodocumento_institucioneducativaid_unique")
        ]

def __str__(self):
    return f'{self.tipodocumento} {self.institucioneducativaid} {self.consecutivo}'
