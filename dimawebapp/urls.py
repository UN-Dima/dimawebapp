"""dimawebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include('dima.urls')),

    path("grupos/", include('groups.urls')),
    path("investigadores/", include('researchers.urls')),
    path("propiedad_intelectual/", include('intellectual_property.urls')),

    path("proyectos/", include('projects.urls')),

    path("", include('visualizations.urls')),
    # path("", include('unal_plantilla_web.urls')),


    path("convocatorias/", include('calls.urls')),

    path("dashboard/", include('dashboard.urls')),




    # Third party modules
    path('tinymce/', include('tinymce.urls')),
    path('.well-known/', include('letsencrypt.urls')),
    # re_path(r'^\.well-known/', include('letsencrypt.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

