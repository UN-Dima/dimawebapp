from django.urls import path
from .views import QuipuProyectView


urlpatterns = [

    path('proyectos/', QuipuProyectView.as_view(), name='proyectos'),
    path('proyectos/<slug:pk>', QuipuProyectView.as_view(), name='proyectos'),

]


