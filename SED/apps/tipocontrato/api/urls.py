from django.urls import path
from apps.tipocontrato.api.api import tipocontrato_api_view, tipocontrato_details_api_view

urlpatterns = [
    path("",tipocontrato_api_view, name= "tipocontrato_api"),
    path("<str:codigo>/",tipocontrato_details_api_view, name= "tipocontrato_details_api_view") 
]