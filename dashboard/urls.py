from django.urls import path, include
from .views import HomeView, DashboardProyectView, download_backup

urlpatterns = [
    path("", HomeView.as_view(), name='dashboard'),
    path("quipu/", include('quipu.urls')),
    path("upload_project/", DashboardProyectView.as_view(), name='upload_project'),
    path("upload_project/download/",download_backup, name='backup'),
]





