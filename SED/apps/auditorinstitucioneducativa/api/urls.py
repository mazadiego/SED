from django.urls import path
from apps.auditorinstitucioneducativa.api.api import auditoriainstitucioneducativa_api_view,auditoriainstitucioneducativa_id_api_view,auditoriainstitucioneducativa_usuarios_api_view

urlpatterns = [
    path("usuario/<str:username>/",auditoriainstitucioneducativa_api_view,name="auditoriainstitucioneducativa_api_view"),
    path("id/<str:id>/",auditoriainstitucioneducativa_id_api_view,name="auditoriainstitucioneducativa_id_api_view"),
    path("listarusuariossinrelacion/",auditoriainstitucioneducativa_usuarios_api_view,name="auditoriainstitucioneducativa_usuarios_api_view")
]
