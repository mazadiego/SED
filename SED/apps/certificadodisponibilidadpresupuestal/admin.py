from atexit import register
from xml.parsers.expat import model
from django.apps import apps
from django.contrib import admin
from .models import Certificadodisponibilidadpresupuestal
# Register your models here.

admin.site.register(Certificadodisponibilidadpresupuestal)
