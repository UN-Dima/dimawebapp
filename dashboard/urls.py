from django.urls import path, include
from .views import HomeView, DashboardProyectView

urlpatterns = [
    path("", HomeView.as_view(), name='dashboard'),
    path("quipu/", include('quipu.urls')),
    path("upload_project/", DashboardProyectView.as_view(), name='upload_project')
]





