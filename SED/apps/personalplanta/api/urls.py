from xml.etree.ElementInclude import include
from django.urls import path
from apps.personalplanta.api.api import personalplanta_api_view, personalplanta_details_api_view,personalplanta_institucioneducativa_details_api_view

urlpatterns = [
    path("",personalplanta_api_view,name="personalplanta_api_view"),
    path("<str:codigo>/",personalplanta_details_api_view,name="personalplanta_details_api_view"),
    path("institucioneducativa/<str:codigo>/",personalplanta_institucioneducativa_details_api_view,name="personalplanta_institucioneducativa_details_api_view")
]
