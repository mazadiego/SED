from xml.etree.ElementInclude import include
from django.urls import path
from apps.solicitudpresupuestalcabecera.api.api import solicitudpresupuestalcabecera_api_view,solicitudpresupuestal_consecutivo_api_view

urlpatterns = [
    path("",solicitudpresupuestalcabecera_api_view,name="solicitudpresupuestalcabecera_api_view"),
    path("consecutivo/",solicitudpresupuestal_consecutivo_api_view,name="solicitudpresupuestal_consecutivo_api_view")
]
