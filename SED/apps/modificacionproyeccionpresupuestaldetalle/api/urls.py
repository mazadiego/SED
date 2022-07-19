from xml.etree.ElementInclude import include
from django.urls import path
from apps.modificacionproyeccionpresupuestaldetalle.api.api import modificacionproyeccionpresupuestaldetalle_api_view

urlpatterns = [
    path("",modificacionproyeccionpresupuestaldetalle_api_view,name="modificacionproyeccionpresupuestaldetalle_api_view")
]
