from django.urls import path
from apps.institucioneducativa.api.api import institucioneducativa_api_view, institucioneducativa_details_api_view, institucioneducativa_usuario_details_api_view

urlpatterns = [
    path("<str:codigo>/",institucioneducativa_usuario_details_api_view, name= "institucioneducativa_usuario_details_api")
]