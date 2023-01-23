from django.urls import path
from .views import Researchers
urlpatterns = [

    path('', Researchers.as_view(), name='researchers'),
    path('<str:obscure>', Researchers.as_view(), name='researchers'),

]


