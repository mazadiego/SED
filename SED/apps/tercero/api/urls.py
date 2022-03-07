from xml.etree.ElementInclude import include
from django.urls import path
from apps.tercero.api.api import tercero_api_view, tercero_details_api_view

urlpatterns = [
    path("",tercero_api_view,name="tercero_api_view"),
    path("tipoidentificacion/",tercero_details_api_view,name="tercero_details_api_view")
]
