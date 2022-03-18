from django.urls import path
from apps.periodo.api.api import periodo_api_view, periodo_details_api_view,periodos_activos_api_view

urlpatterns = [
    path("",periodo_api_view, name= "periodo_api"),
    path("<str:periodo>/",periodo_details_api_view, name= "periodo_details_api_view"), 
    path("listar/activos/",periodos_activos_api_view, name= "periodos_activos_api_view")
]