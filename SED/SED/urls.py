"""SED URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.views.static import serve

schema_view = get_schema_view(
   openapi.Info(
      title="SED API",
      default_version='v 0.1',
      description="SED - Presupuesto",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('usuario/',include('apps.usuario.api.urls')),
    path('institucioneducativa/',include('apps.institucioneducativa.api.urls')),
    path('tiporecaudo/',include('apps.tiporecaudo.api.urls')),
    path('tipocontrato/',include('apps.tipocontrato.api.urls')),
    path('personalplanta/',include('apps.personalplanta.api.urls')),
    path('tipoidentificacion/',include('apps.tipoidentificacion.api.urls')),
    path('tercero/',include('apps.tercero.api.urls')),
    path('rubropresupuestal/',include('apps.rubropresupuestal.api.urls')),
    path('fuenterecurso/',include('apps.fuenterecurso.api.urls')),
    path('periodo/',include('apps.periodo.api.urls')),
    path('proyeccionpresupuestalcabecera/',include('apps.proyeccionpresupuestalcabecera.api.urls')),
    path('proyeccionpresupuestaldetalle/',include('apps.proyeccionpresupuestaldetalle.api.urls')),
    path('ingresopresupuestal/',include('apps.ingresopresupuestal.api.urls')),
    path('recaudopresupuestal/',include('apps.recaudopresupuestal.api.urls')),
    path('solicitudpresupuestalcabecera/',include('apps.solicitudpresupuestalcabecera.api.urls')),
    path('solicitudpresupuestaldetalle/',include('apps.solicitudpresupuestaldetalle.api.urls')),
    path('certificadodisponibilidadpresupuestal/',include('apps.certificadodisponibilidadpresupuestal.api.urls')),
    path('registropresupuestal/',include('apps.registropresupuestal.api.urls')),
    path('obligacionpresupuestal/',include('apps.obligacionpresupuestal.api.urls')),
    path('pagopresupuestal/',include('apps.pagopresupuestal.api.urls')),
    path('modificacionproyeccionpresupuestalcabecera/',include('apps.modificacionproyeccionpresupuestalcabecera.api.urls')),
    path('modificacionproyeccionpresupuestaldetalle/',include('apps.modificacionproyeccionpresupuestaldetalle.api.urls')),
    path('adjuntos/',include('apps.adjuntos.api.urls')),
    path('auditorinstitucioneducativa/',include('apps.auditorinstitucioneducativa.api.urls')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$',serve,{
        'document_root': settings.MEDIA_ROOT,
    })
]