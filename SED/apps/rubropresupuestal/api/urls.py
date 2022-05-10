from xml.etree.ElementInclude import include
from django.urls import path
from apps.rubropresupuestal.api.api import rubropresupuestal_api_view, rubropresupuestal_details_api_view,rubropresupuestal_final_api_view,saldorubroporproyeccion_final_api_view


urlpatterns = [
    path("",rubropresupuestal_api_view,name="rubropresupuestal_api_view"),
    path("<str:codigo>/",rubropresupuestal_details_api_view,name="rubropresupuestal_details_api_view"),
    path("detalle/final/",rubropresupuestal_final_api_view,name="rubropresupuestal_final_api_view"),
    path("detalle/saldoporproyeccion/",saldorubroporproyeccion_final_api_view,name="saldorubroporproyeccion_final_api_view")
]
