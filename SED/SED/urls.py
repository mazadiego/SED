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
from django.urls import path, include

urlpatterns = [
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
]
