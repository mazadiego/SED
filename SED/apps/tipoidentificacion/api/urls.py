from django.urls import path
from apps.tipoidentificacion.api.api import tipoidentificacion_api_view, tipoidentificacion_details_api_view

urlpatterns = [
    path("",tipoidentificacion_api_view, name= "tipoidentificacion_api"),
    path("<str:codigo>/",tipoidentificacion_details_api_view, name= "tipoidentificacion_details_api_view") 
]