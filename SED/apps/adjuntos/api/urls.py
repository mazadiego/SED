from django.urls import path
from apps.adjuntos.api.api import adjuntos_api_view,adjuntos_api_id_view,adjuntos_api_descargar_id_view


urlpatterns = [
    path("",adjuntos_api_view, name= "adjuntos_api_view"),
    path("id/<str:id>",adjuntos_api_id_view, name= "adjuntos_api_id_view"),
    path("descargar/<str:id>",adjuntos_api_descargar_id_view    , name= "adjuntos_api_descargar_id_view    ")
]

