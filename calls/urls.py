from django.urls import path
from .views import CallsView, JointCallView, MincienciasCallView, StudentsCallView, InternalCallView


urlpatterns = [

    path('', CallsView.as_view(), name='calls'),
    path('internas', InternalCallView.as_view(), name='internal_call'),
    path('internas/<slug:pk>', InternalCallView.as_view(), name='internal_call'),

    path('conjuntas', JointCallView.as_view(), name='joint_call'),
    path('conjuntas/<slug:pk>', JointCallView.as_view(), name='joint_call'),

    path('minciencias', MincienciasCallView.as_view(), name='minciencias_call'),
    path('minciencias/<slug:pk>', MincienciasCallView.as_view(), name='minciencias_call'),

    path('estudiantes_auxiliares', StudentsCallView.as_view(), name='students_call'),
    path('estudiantes_auxiliares/<slug:pk>', StudentsCallView.as_view(), name='students_call'),

    path('lista', CallsView.as_view(), name='calls_list'),
]



