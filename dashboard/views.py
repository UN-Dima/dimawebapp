import os
from datetime import datetime

from django.views.generic.base import TemplateView
from django.http import JsonResponse

from projects.models import Project
from quipu.models import Resources_QuipuProject, Row_QuipuProject
from utils import nan_2_zero
from utils.xml_scraper import load_projects_xls
from dimawebapp.settings import DATABASES

########################################################################
class HomeView(TemplateView):
    template_name = "dashboard/home.html"

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)
        return context

class DashboardProyectView(TemplateView):

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        context = self.get_context_data(**kwargs)

        if pk:
            context['project'] = Project.objects.get(pk=pk)
            context['project_admin'] = Project._meta
            self.template_name = "proyectos_quipu_view.html"
        else:
            context['projects'] = Project.objects.all()
            context['projects_admin'] = Project._meta
            self.template_name = "dashboard/upload_projects.html"

        return self.render_to_response(context)

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        """"""
        messages = []
        for file in request.FILES.getlist('xmlfile'):
            print(file.name)
            if file.name.lower().endswith('.xls'):
                df, report_date = load_projects_xls(file)
                os.system(f'cp "{DATABASES["default"]["NAME"]}" "{DATABASES["default"]["NAME"][:-8]}_{datetime.now()}.sqlite3"')
                status, msg = self.save_report(df)
                if status:
                    messages.append(f'Cargado: {file.name}')
                else:
                    messages.append(f'Falló: {file.name}')
                    messages.append(f'Error: {msg}')
            else:
                messages.append(f'Archivo no soportado: {file.name}')

        return JsonResponse({'msg': messages})

    # ----------------------------------------------------------------------
    def save_report(self, report):
        """"""

        try:
            for project in report:
                researcher = project['INVESTIGADOR PRINCIPAL'].split(' ')
                last_names = researcher[-2] +' '+ researcher[-1]
                researcher.pop(-1)
                researcher.pop(-1)
                first_names = researcher[0]
                for name in researcher[1:]:
                    first_names += ' '+name
                if Project.objects.filter(pk=project['CÓDIGO HERMES']).count():
                    p = Project.objects.get(pk=project['CÓDIGO HERMES'])
                    p.quipu_cod_0 = project['CÓDIGO QUIPÚ']
                    p.project_name = project['NOMBRE PROYECTO']
                    p.project_state = project['ESTADO ACTUAL']
                    p.call_type = project['TIPO']
                    p.call = project['CONVOCATORIA']
                    p.modality = project['MODALIDAD']
                    p.professor_id = project['IDENTIFICACIÓN INVESTIGADOR PRINCIPAL']
                    p.first_name = first_names
                    p.last_name = last_names
                    p.email = project['E-MAIL INVESTIGADOR PRINCIPAL']
                    p.departament = project['DEPARTAMENTO O INSTITUTO - INVESTIGADOR PRINCIPAL']
                    p.faculty = project['FACULTAD - INVESTIGADOR PRINCIPAL']
                    p.start_date = project['FECHA INICIO']
                    p.end_date = project['FECHA FINAL CON PRÓRROGAS']
                    total_resources = nan_2_zero(float(project['TOTAL RECURSOS INTERNOS'])) + nan_2_zero(float(project['TOTAL RECURSOS FINANCIADORAS EXTERNAS']))
                    p.total_project = total_resources
                    p.total_appropriation = 0 #project['CÓDIGO QUIPÚ']

                    #Now we find the Quipu Data
                    qr = Resources_QuipuProject.objects.filter(proyecto_id = project['CÓDIGO QUIPÚ'])
                    s = 0
                    for resource in qr:
                        q = Row_QuipuProject.objects.filter(resource_id = resource.id)
                        last_imp = str(max([int(imp.imputacion) for imp in q]))
                        saldo = Row_QuipuProject.objects.filter(resource_id = resource.id,
                                                                 imputacion = last_imp).saldo_por_comprometer
                        s += float(saldo)
                    p.total_commitment_balance = s
                    p.executed = total_resources - s
                    p.execution_percentage = (total_resources - s)/total_resources
                    #p.save()
                else:
                    new_project = {
                        'hermes_cod':project['CÓDIGO HERMES'],
                        'quipu_cod_0':project['CÓDIGO QUIPÚ'],
                        'project_name':project['NOMBRE PROYECTO'],
                        'project_state':project['ESTADO ACTUAL'],
                        'call_type':project['TIPO'],
                        'call':project['CONVOCATORIA'],
                        'modality':project['MODALIDAD'],
                        'professor_id':project['IDENTIFICACIÓN INVESTIGADOR PRINCIPAL'],
                        'first_name':first_names,
                        'last_name':last_names,
                        'email':project['E-MAIL INVESTIGADOR PRINCIPAL'],
                        'departament':project['DEPARTAMENTO O INSTITUTO - INVESTIGADOR PRINCIPAL'],
                        'faculty':project['FACULTAD - INVESTIGADOR PRINCIPAL'],
                        'start_date':project['FECHA INICIO'],
                        'end_date':project['FECHA FINAL CON PRÓRROGAS'],
                        'total_project':0,
                        'total_appropriation':0,
                        'executed':project['VALOR EJECUTADO'],
                        'total_commitment_balance':0,
                        'execution_percentage':0,
                    }
                    p = Project.objects.create(**new_project)

            return True, ''
        except Exception as e:
            return False, e
