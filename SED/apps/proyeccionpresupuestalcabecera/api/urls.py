from xml.etree.ElementInclude import include
from django.urls import path
from apps.proyeccionpresupuestalcabecera.api.api import proyeccionpresupuestalcabecera_api_view

urlpatterns = [
    path("",proyeccionpresupuestalcabecera_api_view,name="proyeccionpresupuestalcabecera_api_view")
    
]
