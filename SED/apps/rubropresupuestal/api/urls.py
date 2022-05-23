from xml.etree.ElementInclude import include
from django.urls import path
from apps.rubropresupuestal.api.api import rubropresupuestal_api_view, rubropresupuestal_details_api_view,rubropresupuestal_final_api_view,saldorubroporproyeccion_final_api_view,rubropresupuestal_proyectados_api_view,saldorubro_solicitud_api_view,saldorubro_recaudo_api_view
from apps.rubropresupuestal.api.api import rubropresupuestal_solicitados_api_view


urlpatterns = [
    path("",rubropresupuestal_api_view,name="rubropresupuestal_api_view"),
    path("<str:codigo>/",rubropresupuestal_details_api_view,name="rubropresupuestal_details_api_view"),
    path("detalle/final/",rubropresupuestal_final_api_view,name="rubropresupuestal_final_api_view"),
    path("detalle/saldoporproyeccion/",saldorubroporproyeccion_final_api_view,name="saldorubroporproyeccion_final_api_view"),
    path("detalle/proyectados/",rubropresupuestal_proyectados_api_view,name="rubropresupuestal_proyectados_api_view"),
    path("detalle/saldosolicitud/",saldorubro_solicitud_api_view,name="saldorubro_solicitud_api_view"),
    path("detalle/saldorecaudo/",saldorubro_recaudo_api_view,name="saldorubro_recaudo_api_view"),
    path("detalle/solicitados/",rubropresupuestal_solicitados_api_view,name="rubropresupuestal_solicitados_api_view"),
]
