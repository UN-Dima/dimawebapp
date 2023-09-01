from django.urls import path
from django.views.generic import TemplateView
from .views import DataView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', DataView.as_view(), name='data'),
    path('tablas', DataView.as_view(), name='tables'),
]


