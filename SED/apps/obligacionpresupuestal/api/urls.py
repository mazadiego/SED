from xml.etree.ElementInclude import include
from django.urls import path
from apps.obligacionpresupuestal.api.api import obligacionpresupuestal_api_view,obligacionpresupuestal_consecutivo_api_view



urlpatterns = [
    path("",obligacionpresupuestal_api_view,name="obligacionpresupuestal_api_view"),
    path("consecutivo/",obligacionpresupuestal_consecutivo_api_view,name="obligacionpresupuestal_consecutivo_api_view")
    
]