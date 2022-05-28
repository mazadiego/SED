from xml.etree.ElementInclude import include
from django.urls import path
from apps.pagopresupuestal.api.api import pagopresupuestal_api_view,pagopresupuestal_consecutivo_api_view



urlpatterns = [
    path("",pagopresupuestal_api_view,name="pagopresupuestal_api_view"),
    path("consecutivo/",pagopresupuestal_consecutivo_api_view,name="pagopresupuestal_consecutivo_api_view")
    
]