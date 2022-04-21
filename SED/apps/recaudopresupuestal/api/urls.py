from xml.etree.ElementInclude import include
from django.urls import path
from apps.recaudopresupuestal.api.api import recaudopresupuestal_api_view,recaudopresupuestal_consecutivo_api_view

urlpatterns = [
    path("",recaudopresupuestal_api_view,name="recaudopresupuestal_api_view"),
    path("consecutivo/",recaudopresupuestal_consecutivo_api_view,name="recaudopresupuestal_consecutivo_api_view")
    
]