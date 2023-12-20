from django.urls import path
from .views import PatentsView, SpinOffView
from dima.views import ContentView


urlpatterns = [

    path('patents/', PatentsView.as_view(), name='patents'),
    path('patents/<slug:pk>', PatentsView.as_view(), name='patents'),
    path('creacion_spin-off', ContentView.as_view(label='spinoff',
         template_name="spinoff.html"), name='spinoff'),
    path('spin-offs', SpinOffView.as_view(), name='spinoff_groups'),

]


