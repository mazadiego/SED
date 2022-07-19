from xml.etree.ElementInclude import include
from django.urls import path
from apps.modificacionproyeccionpresupuestalcabecera.api.api import modificacionproyeccionpresupuestalcabecera_api_view

urlpatterns = [
    path("",modificacionproyeccionpresupuestalcabecera_api_view,name="modificacionproyeccionpresupuestalcabecera_api_view")
    
]
