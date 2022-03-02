from django.urls import path
from apps.tiporecaudo.api.api import tiporecaudo_api_view, tiporecaudo_details_api_view

urlpatterns = [
    path("",tiporecaudo_api_view, name= "tiporecaudo_api"),
    path("<str:codigo>/",tiporecaudo_details_api_view, name= "tiporecaudo_details_api_view") 
]