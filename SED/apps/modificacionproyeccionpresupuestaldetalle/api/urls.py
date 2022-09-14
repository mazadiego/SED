from xml.etree.ElementInclude import include
from django.urls import path
from apps.modificacionproyeccionpresupuestaldetalle.api.api import modificacionproyeccionpresupuestaldetalle_api_view,modificacionproyeccionpresupuestaldetalle_id_api_view

urlpatterns = [
    path("",modificacionproyeccionpresupuestaldetalle_api_view,name="modificacionproyeccionpresupuestaldetalle_api_view"),
    path("<str:id>/",modificacionproyeccionpresupuestaldetalle_id_api_view,name="modificacionproyeccionpresupuestaldetalle_id_api_view")
    
]
