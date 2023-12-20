from django.urls import path
from .views import SeminarView

urlpatterns = [
    path('', SeminarView.as_view(), name='seminar'),
    path('<slug:pk>', SeminarView.as_view(), name='seminar'),
]
