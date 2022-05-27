from xml.etree.ElementInclude import include
from django.urls import path
from apps.registropresupuestal.api.api import registropresupuestal_api_view,registropresupuestal_consecutivo_api_view,rp_saldopor_op_api_view


urlpatterns = [
    path("",registropresupuestal_api_view,name="registropresupuestal_api_view"),
    path("consecutivo/",registropresupuestal_consecutivo_api_view,name="registropresupuestal_consecutivo_api_view"),
    path("consecutivo/saldo/",rp_saldopor_op_api_view,name="rp_saldopor_op_api_view") 
]