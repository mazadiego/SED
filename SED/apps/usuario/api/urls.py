from django.urls import path
from apps.usuario.api.api import usuario_api_view, usuario_details_api_view

urlpatterns = [
    path("",usuario_api_view, name= "usuario_api"),
    path("<str:codigo>/",usuario_details_api_view, name= "usuario_details_api_view") 
]