from xml.etree.ElementInclude import include
from django.urls import path
from apps.certificadodisponibilidadpresupuestal.api.api import certificadodisponibilidadpresupuestal_api_view,certificadodisponibilidadpresupuestal_consecutivo_api_view


urlpatterns = [
    path("",certificadodisponibilidadpresupuestal_api_view,name="certificadodisponibilidadpresupuestal_api_view"),
    path("consecutivo/",certificadodisponibilidadpresupuestal_consecutivo_api_view,name="certificadodisponibilidadpresupuestal_consecutivo_api_view")
    
]