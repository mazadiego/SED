from xml.etree.ElementInclude import include
from django.urls import path
from apps.solicitudpresupuestaldetalle.api.api import solicitudpresupuestaldetalle_api_view,solicitudpresupuestaldetalle_id_api_view

urlpatterns = [
    path("",solicitudpresupuestaldetalle_api_view,name="solicitudpresupuestaldetalle_api_view"),
    path("<str:id>/",solicitudpresupuestaldetalle_id_api_view,name="solicitudpresupuestaldetalle_id_api_view")    
]
