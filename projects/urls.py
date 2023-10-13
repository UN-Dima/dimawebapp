from django.urls import path
from .views import Projects, Project_Report, project_report
urlpatterns = [

    path('', Projects.as_view(), name='projects'),
    path('<str:obscure>', Projects.as_view(), name='projects'),
    path('<str:obscure>/report', Project_Report.as_view(), name='report'),
    path('<str:obscure>/report/pdf', project_report, name='report'),

]


