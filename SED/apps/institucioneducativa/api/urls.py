from django.urls import path
from apps.institucioneducativa.api.api import institucioneducativa_api_view, institucioneducativa_details_api_view, institucioneducativa_usuario_details_api_view

urlpatterns = [
    path("",institucioneducativa_api_view, name= "institucioneducativa_api"),
    path("<str:codigo>/",institucioneducativa_details_api_view, name= "institucioneducativa_details_api"), 
    path("usuario/<str:username>/",institucioneducativa_usuario_details_api_view, name= "institucioneducativa_usuario_details_api")
]