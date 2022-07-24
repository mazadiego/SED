from xml.etree.ElementInclude import include
from django.urls import path
from apps.proyeccionpresupuestaldetalle.api.api import proyeccionpresupuestaldetalle_api_view,proyeccionpresupuestaldetalle_all_api_view

urlpatterns = [
    path("",proyeccionpresupuestaldetalle_api_view,name="proyeccionpresupuestaldetalle_api_view"),
    path("todos/",proyeccionpresupuestaldetalle_all_api_view,name="proyeccionpresupuestaldetalle_all_api_view")
]
