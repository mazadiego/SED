from django.db import models
from apps.institucioneducativa.models import Institucioneducativa
from apps.usuario.models import Usuario
# Create your models here.

class Auditoriainstitucioneducativa(models.Model):
    institucioneducativaid = models.ForeignKey(Institucioneducativa,on_delete=models.RESTRICT)
    usuarioid = models.ForeignKey(Usuario,on_delete=models.RESTRICT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucioneducativaid','usuarioid'], name="UK_institucioneducativaid_usuarioid_unique")
        ]

def __str__(self):
    return f'{self.institucioneducativaid} {self.usuarioid}'


