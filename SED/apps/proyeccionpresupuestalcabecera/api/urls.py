from xml.etree.ElementInclude import include
from django.urls import path
from apps.proyeccionpresupuestalcabecera.api.api import proyeccionpresupuestalcabecera_api_view,proyeccionpresupuestal_Aprobar_api_view

urlpatterns = [
    path("",proyeccionpresupuestalcabecera_api_view,name="proyeccionpresupuestalcabecera_api_view"),
    path("aprobar/",proyeccionpresupuestal_Aprobar_api_view,name="proyeccionpresupuestal_Aprobar_api_view")
    
]
