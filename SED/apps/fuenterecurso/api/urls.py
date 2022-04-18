from xml.etree.ElementInclude import include
from django.urls import path
from apps.fuenterecurso.api.api import fuenterecurso_api_view, fuenterecurso_details_api_view, fuenterecurso_final_api_view,fuenterecurso_proyeccion_api_view,saldofuenterecursoporingreso_api_view


urlpatterns = [
    path("",fuenterecurso_api_view,name="personalplanta_api_view"),
    path("<str:codigo>/",fuenterecurso_details_api_view,name="fuenterecurso_details_api_view"),
    path("detalle/final/",fuenterecurso_final_api_view,name="fuenterecurso_final_api_view"),
    path("proyeccion/<str:codigoinstitucioneducativa>/",fuenterecurso_proyeccion_api_view,name="fuenterecurso_proyeccion_api_view"),
    path("fuenterecursoporingreso/saldo/",saldofuenterecursoporingreso_api_view,name="saldofuenterecursoporingreso_api_view"),
]
