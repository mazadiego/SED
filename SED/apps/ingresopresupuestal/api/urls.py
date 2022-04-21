from xml.etree.ElementInclude import include
from django.urls import path
from apps.ingresopresupuestal.api.api import ingresopresupuestal_api_view,ingresopresupuestal_consecutivo_api_view,ingresopresupuestalsaldoporrecaudo_api_view

urlpatterns = [
    path("",ingresopresupuestal_api_view,name="ingresopresupuestal_api_view"),
    path("consecutivo/",ingresopresupuestal_consecutivo_api_view,name="ingresopresupuestal_consecutivo_api_view"),
    path("consecutivo/saldo/",ingresopresupuestalsaldoporrecaudo_api_view,name="ingresopresupuestalsaldoporrecaudo_api_view")
]