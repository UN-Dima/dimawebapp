import os
from datetime import datetime
import re

from django.views.generic.base import TemplateView
from django.http import JsonResponse, FileResponse
from django.core.exceptions import PermissionDenied

from projects.models import Project
from groups.models import ResearchGroup
from quipu.models import Resources_QuipuProject, Row_QuipuProject
from utils import nan_2_zero
from utils.xml_scraper import load_projects_xls
from dimawebapp.settings import DATABASES

OLD_DB = ''
########################################################################
class HomeView(TemplateView):
    template_name = "dashboard/home.html"

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)
        return context

def download_backup(request, obscure=None, *args, **kwargs):
    global OLD_DB
    old_database = OLD_DB
    OLD_DB = None
    if request.user.is_authenticated:
        return FileResponse(open(f'{old_database}.sqlite3','rb'), as_attachment=True,
                        filename=f'{old_database}.sqlite3')
    else:
        raise PermissionDenied

########################################################################
class DashboardProyectView(TemplateView):

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        context = self.get_context_data(**kwargs)

        if pk:
            context['project'] = Project.objects.get(pk=pk)
            context['project_admin'] = Project._meta
            self.template_name = "projects_view.html"
        else:
            context['projects'] = Project.objects.all()
            context['projects_admin'] = Project._meta
            self.template_name = "dashboard/upload_projects.html"

        return self.render_to_response(context)

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        """"""
        global OLD_DB
        messages = []
        response = {}
        for file in request.FILES.getlist('xmlfile'):
            if file.name.lower().endswith('.xls'):
                df, report_date = load_projects_xls(file)
                OLD_DB = f'{DATABASES["default"]["NAME"][:-8]}_{datetime.now()}'
                os.system(f'cp "{DATABASES["default"]["NAME"]}" "{OLD_DB}.sqlite3"')
                response['redirect'] = f'/dashboard/download/'
                status, msg = self.save_report(df)
                if status:
                    messages.append(f'Cargado: {file.name}')
                else:
                    messages.append(f'Falló: {file.name}')
                    messages.append(f'Error: {msg}')
            else:
                messages.append(f'Archivo no soportado: {file.name}')
        response['msg'] = messages
        return JsonResponse(response)
    def foo(self, request, *args, **kwargs):
        print('Hello, World!')
        print(request)
    # ----------------------------------------------------------------------
    def save_report(self, report):
        """"""
        departaments = {
            '4- DEPARTAMENTO DE ADMINISTRACIÓN': 'departament_0001',
            '4- DEPARTAMENTO DE CIENCIAS HUMANAS': 'departament_0002',
            '4- DEPARTAMENTO DE FÍSICA Y QUÍMICA': 'departament_0003',
            '4- DEPARTAMENTO DE INFORMÁTICA Y COMPUTACIÓN': 'departament_0004',
            '4- DEPARTAMENTO DE INGENIERÍA CIVIL': 'departament_0005',
            '4- DEPARTAMENTO DE INGENIERÍA ELÉCTRICA, ELECTRÓNICA Y COMPUTACIÓN': 'departament_0006',
            '4- DEPARTAMENTO DE INGENIERÍA INDUSTRIAL': 'departament_0007',
            '4- DEPARTAMENTO DE INGENIERÍA QUÍMICA': 'departament_0008',
            '4- DEPARTAMENTO DE MATEMÁTICAS': 'departament_0009',
            '4- ESCUELA DE ARQUITECTURA Y URBANISMO': 'departament_0010',
        }

        states = {
            'Activo':'project_state_0001', #Starting here are the true labels
            'Finalizado':'project_state_0002',
            'No aprobado':'project_state_0003',
            'Propuesto':'project_state_0004', 
            'Suspendido':'project_state_0006',
            'No cumplió requisitos':'project_state_0003', #Starting here are inferred labels
            'Por finalizar entidad externa':'project_state_0005',
            'Ingresando Proyecto':'project_state_0004',
            'Aprobado':'project_state_0004',
            'Banco de proyectos':'project_state_0002',
            'Cancelado':'project_state_0002',
            'Elegible':'project_state_0004',
            'En Legalización':'project_state_0004',
            'Aprobado por OCAD':'project_state_0004',
        }
        c_types = {
            'SEDE':'call_type_0002',
            'NACIONAL':'call_type_0001',
            0:'call_type_0004',
            'FACULTAD':'call_type_0002',
        }
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
                    p.quipu_cod_0 = int(nan_2_zero(project['CÓDIGO QUIPÚ']))
                    p.project_name = project['NOMBRE PROYECTO']
                    state = project['ESTADO ACTUAL']
                    p.project_state = states[state]
                    c_type = nan_2_zero(project['TIPO DE CONVOCATORIA'])
                    p.call_type = c_types[c_type]
                    p.call = project['CONVOCATORIA']
                    p.modality = project['MODALIDAD']
                    p.professor_id = re.search('[0-9]+',project['IDENTIFICACIÓN INVESTIGADOR PRINCIPAL']).group()
                    p.first_name = first_names
                    p.last_name = last_names
                    p.email = project['E-MAIL INVESTIGADOR PRINCIPAL']
                    depar = project['DEPARTAMENTO O INSTITUTO - INVESTIGADOR PRINCIPAL']
                    print('Cake')
                    if not depar in departaments.keys():
                        p.departament = 'departament_0011'
                    else:
                        p.departament = departaments[depar]
                    faculty = str(nan_2_zero(project['FACULTAD - INVESTIGADOR PRINCIPAL']))
                    if 'INGE' in faculty:
                        faculty = 'faculty_0003'
                    elif 'ADMIN' in faculty:
                        faculty = 'faculty_0001'
                    elif 'NATURAL' in faculty:
                        faculty = 'faculty_0002'
                    else:
                        faculty = 'faculty_0004'
                    p.faculty = faculty
                    print('Icecream')
                    if type(project['FECHA INICIO']) == str:
                        p.start_date = datetime.strptime(project['FECHA INICIO'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
                    else:
                        p.start_date = float('nan')
                    if type(project['FECHA FINAL CON PRÓRROGAS']) == str:
                        p.end_date = datetime.strptime(project['FECHA FINAL CON PRÓRROGAS'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
                    else:
                        p.end_date = float('nan')
                    total_resources = nan_2_zero(float(project['TOTAL RECURSOS INTERNOS'])) + nan_2_zero(float(project['TOTAL RECURSOS FINANCIADORAS EXTERNAS']))
                    p.total_project = total_resources
                    #Now we find the Quipu Data
                    qr = Resources_QuipuProject.objects.filter(proyecto_id = project['CÓDIGO QUIPÚ'])
                    s = 0
                    s2 = 0
                    for resource in qr:
                        q = Row_QuipuProject.objects.filter(resource_id = resource.id)
                        last_imp = str(max([int(imp.imputacion) for imp in q]))
                        saldo = Row_QuipuProject.objects.filter(resource_id = resource.id,
                                                                 imputacion = last_imp)[0].saldo_por_comprometer
                        s += float(saldo)

                    p.total_appropriation = s2 #project['CÓDIGO QUIPÚ']
                    p.total_commitment_balance = s
                    p.executed = total_resources - s
                    if total_resources:
                        p.execution_percentage = (total_resources - s)/total_resources
                    else:
                        p.execution_percentage = 0
                    quipu_code_1 = p.quipu_cod_1
                    if quipu_code_1:
                        quipu_code_1 = str(quipu_code_1).split(' ')[0]
                    if p.quipu_cod_1 == 'no esta':
                        p.quipu_cod_1 = None
                    else:
                        p.quipu_cod_1 = quipu_code_1
                    p.save()
                else:
                    total_resources = nan_2_zero(float(project['TOTAL RECURSOS INTERNOS'])) + nan_2_zero(float(project['TOTAL RECURSOS FINANCIADORAS EXTERNAS']))
                    faculty = str(nan_2_zero(project['FACULTAD - INVESTIGADOR PRINCIPAL']))
                    if 'INGE' in faculty:
                        faculty = 'faculty_0003'
                    elif 'ADMIN' in faculty:
                        faculty = 'faculty_0001'
                    elif 'NATURAL' in faculty:
                        faculty = 'faculty_0002'
                    else:
                        faculty = 'faculty_0004'
                    depar = project['DEPARTAMENTO O INSTITUTO - INVESTIGADOR PRINCIPAL']
                    if not depar in departaments.keys():
                        departament = 'departament_0011'
                    else:
                        departament = departaments[depar]
                    #Now we find the Quipu Data
                    qr = Resources_QuipuProject.objects.filter(proyecto_id = project['CÓDIGO QUIPÚ'])
                    s = 0
                    s2 = 0
                    for resource in qr:
                        q = Row_QuipuProject.objects.filter(resource_id = resource.id)
                        last_imp = str(max([int(imp.imputacion) for imp in q]))
                        saldo = Row_QuipuProject.objects.filter(resource_id = resource.id,
                                                                 imputacion = last_imp)[0].saldo_por_comprometer
                        s += float(saldo)
                    if total_resources:
                        execution_percentage = (total_resources - s)/total_resources
                    else:
                        execution_percentage = 0
                    
                    if type(project['FECHA INICIO']) == str:
                        start_date = datetime.strptime(project['FECHA INICIO'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
                    else:
                        start_date = float('nan')
                    if type(project['FECHA FINAL CON PRÓRROGAS']) == str:
                        end_date = datetime.strptime(project['FECHA FINAL CON PRÓRROGAS'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
                    else:
                        end_date = float('nan')
                    new_project = {
                        'hermes_cod':project['CÓDIGO HERMES'],
                        'quipu_cod_0':int(nan_2_zero(project['CÓDIGO QUIPÚ'])),
                        'project_name':project['NOMBRE PROYECTO'],
                        'project_state':states[project['ESTADO ACTUAL']],
                        'call_type':c_types[nan_2_zero(project['TIPO DE CONVOCATORIA'])],
                        'call':project['CONVOCATORIA'],
                        'modality':project['MODALIDAD'],
                        'professor_id':re.search('[0-9]+',project['IDENTIFICACIÓN INVESTIGADOR PRINCIPAL']).group(),
                        'first_name':first_names,
                        'last_name':last_names,
                        'email':project['E-MAIL INVESTIGADOR PRINCIPAL'],
                        'departament':departament,
                        'faculty':faculty,
                        'start_date':start_date,
                        'end_date':end_date,
                        'total_project':total_resources,
                        'total_appropriation':s2,
                        'executed':s,
                        'total_commitment_balance':total_resources - s,
                        'execution_percentage':execution_percentage,
                    }
                    p = Project.objects.create(**new_project)

            return True, ''
        except Exception as e:
            print(project)
            return False, e
########################################################################

class DashboardGroupView(TemplateView):

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        context = self.get_context_data(**kwargs)

        if pk:
            context['project'] = ResearchGroup.objects.get(pk=pk)
            context['project_admin'] = ResearchGroup._meta
            self.template_name = "group_view.html"
        else:
            context['projects'] = ResearchGroup.objects.all()
            context['projects_admin'] = ResearchGroup._meta
            self.template_name = "dashboard/upload_groups.html"

        return self.render_to_response(context)

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        """"""
        if request.idk[:x] == 'http://hermes.unal.edu.co' and request.user.is_authenticated:
            print('foo')
        else:
            print('dee')
#     # ----------------------------------------------------------------------
#     def save_report(self, report):
#         """"""
#         departaments = {
#             '4- DEPARTAMENTO DE ADMINISTRACIÓN': 'departament_0001',
#             '4- DEPARTAMENTO DE CIENCIAS HUMANAS': 'departament_0002',
#             '4- DEPARTAMENTO DE FÍSICA Y QUÍMICA': 'departament_0003',
#             '4- DEPARTAMENTO DE INFORMÁTICA Y COMPUTACIÓN': 'departament_0004',
#             '4- DEPARTAMENTO DE INGENIERÍA CIVIL': 'departament_0005',
#             '4- DEPARTAMENTO DE INGENIERÍA ELÉCTRICA, ELECTRÓNICA Y COMPUTACIÓN': 'departament_0006',
#             '4- DEPARTAMENTO DE INGENIERÍA INDUSTRIAL': 'departament_0007',
#             '4- DEPARTAMENTO DE INGENIERÍA QUÍMICA': 'departament_0008',
#             '4- DEPARTAMENTO DE MATEMÁTICAS': 'departament_0009',
#             '4- ESCUELA DE ARQUITECTURA Y URBANISMO': 'departament_0010',
#         }

#         states = {
#             'Activo':'project_state_0001', #Starting here are the true labels
#             'Finalizado':'project_state_0002',
#             'No aprobado':'project_state_0003',
#             'Propuesto':'project_state_0004', 
#             'Suspendido':'project_state_0006',
#             'No cumplió requisitos':'project_state_0003', #Starting here are inferred labels
#             'Por finalizar entidad externa':'project_state_0005',
#             'Ingresando Proyecto':'project_state_0004',
#             'Aprobado':'project_state_0004',
#             'Banco de proyectos':'project_state_0002',
#             'Cancelado':'project_state_0002',
#             'Elegible':'project_state_0004',
#             'En Legalización':'project_state_0004',
#             'Aprobado por OCAD':'project_state_0004',
#         }
#         c_types = {
#             'SEDE':'call_type_0002',
#             'NACIONAL':'call_type_0001',
#             float('nan'):'call_type_0004',
#             'FACULTAD':'call_type_0002',
#         }
#         try:
#             for project in report:
#                 researcher = project['INVESTIGADOR PRINCIPAL'].split(' ')
#                 last_names = researcher[-2] +' '+ researcher[-1]
#                 researcher.pop(-1)
#                 researcher.pop(-1)
#                 first_names = researcher[0]
#                 for name in researcher[1:]:
#                     first_names += ' '+name

#                 if Project.objects.filter(pk=project['CÓDIGO HERMES']).count():
#                     p = Project.objects.get(pk=project['CÓDIGO HERMES'])
#                     p.quipu_cod_0 = int(nan_2_zero(project['CÓDIGO QUIPÚ']))
#                     p.project_name = project['NOMBRE PROYECTO']
#                     state = project['ESTADO ACTUAL']
#                     p.project_state = states[state]
#                     c_type = project['TIPO DE CONVOCATORIA']
#                     p.call_type = c_types[c_type]
#                     p.call = project['CONVOCATORIA']
#                     p.modality = project['MODALIDAD']
#                     p.professor_id = re.search('[0-9]+',project['IDENTIFICACIÓN INVESTIGADOR PRINCIPAL']).group()
#                     p.first_name = first_names
#                     p.last_name = last_names
#                     p.email = project['E-MAIL INVESTIGADOR PRINCIPAL']
#                     depar = project['DEPARTAMENTO O INSTITUTO - INVESTIGADOR PRINCIPAL']
#                     p.departament = departaments[depar]
#                     faculty = project['FACULTAD - INVESTIGADOR PRINCIPAL']
#                     if 'INGE' in faculty:
#                         faculty = 'faculty_0003'
#                     elif 'ADMIN' in faculty:
#                         faculty = 'faculty_0001'
#                     elif 'NATURAL' in faculty:
#                         faculty = 'faculty_0002'
#                     else:
#                         faculty = 'faculty_0004'
#                     p.faculty = faculty
#                     if type(project['FECHA INICIO']) == str:
#                         p.start_date = datetime.strptime(project['FECHA INICIO'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
#                     else:
#                         p.start_date = float('nan')
#                     if type(project['FECHA FINAL CON PRÓRROGAS']) == str:
#                         p.end_date = datetime.strptime(project['FECHA FINAL CON PRÓRROGAS'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
#                     else:
#                         p.end_date = float('nan')
#                     total_resources = nan_2_zero(float(project['TOTAL RECURSOS INTERNOS'])) + nan_2_zero(float(project['TOTAL RECURSOS FINANCIADORAS EXTERNAS']))
#                     p.total_project = total_resources

#                     #Now we find the Quipu Data
#                     qr = Resources_QuipuProject.objects.filter(proyecto_id = project['CÓDIGO QUIPÚ'])
#                     s = 0
#                     s2 = 0
#                     for resource in qr:
#                         q = Row_QuipuProject.objects.filter(resource_id = resource.id)
#                         last_imp = str(max([int(imp.imputacion) for imp in q]))
#                         saldo = Row_QuipuProject.objects.filter(resource_id = resource.id,
#                                                                  imputacion = last_imp)[0].saldo_por_comprometer
#                         s += float(saldo)

#                     p.total_appropriation = s2 #project['CÓDIGO QUIPÚ']
#                     p.total_commitment_balance = s
#                     p.executed = total_resources - s
#                     if total_resources:
#                         p.execution_percentage = (total_resources - s)/total_resources
#                     else:
#                         p.execution_percentage = 0
#                     quipu_code_1 = p.quipu_cod_1
#                     if quipu_code_1:
#                         quipu_code_1 = str(quipu_code_1).split(' ')[0]
#                     if p.quipu_cod_1 == 'no esta':
#                         p.quipu_cod_1 = None
#                     else:
#                         p.quipu_cod_1 = quipu_code_1
#                     p.save()
#                 else:
#                     total_resources = nan_2_zero(float(project['TOTAL RECURSOS INTERNOS'])) + nan_2_zero(float(project['TOTAL RECURSOS FINANCIADORAS EXTERNAS']))
#                     faculty = project['FACULTAD - INVESTIGADOR PRINCIPAL']
#                     if 'INGE' in faculty:
#                         faculty = 'faculty_0003'
#                     elif 'ADMIN' in faculty:
#                         faculty = 'faculty_0001'
#                     elif 'NATURAL' in faculty:
#                         faculty = 'faculty_0002'
#                     else:
#                         faculty = 'faculty_0004'

#                     #Now we find the Quipu Data
#                     qr = Resources_QuipuProject.objects.filter(proyecto_id = project['CÓDIGO QUIPÚ'])
#                     s = 0
#                     s2 = 0
#                     for resource in qr:
#                         q = Row_QuipuProject.objects.filter(resource_id = resource.id)
#                         last_imp = str(max([int(imp.imputacion) for imp in q]))
#                         saldo = Row_QuipuProject.objects.filter(resource_id = resource.id,
#                                                                  imputacion = last_imp)[0].saldo_por_comprometer
#                         s += float(saldo)
#                     if total_resources:
#                         execution_percentage = (total_resources - s)/total_resources
#                     else:
#                         execution_percentage = 0
                    
#                     if type(project['FECHA INICIO']) == str:
#                         start_date = datetime.strptime(project['FECHA INICIO'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
#                     else:
#                         start_date = float('nan')
#                     if type(project['FECHA FINAL CON PRÓRROGAS']) == str:
#                         end_date = datetime.strptime(project['FECHA FINAL CON PRÓRROGAS'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
#                     else:
#                         end_date = float('nan')
#                     new_project = {
#                         'hermes_cod':project['CÓDIGO HERMES'],
#                         'quipu_cod_0':int(nan_2_zero(project['CÓDIGO QUIPÚ'])),
#                         'project_name':project['NOMBRE PROYECTO'],
#                         'project_state':states[project['ESTADO ACTUAL']],
#                         'call_type':c_types[project['TIPO DE CONVOCATORIA']],
#                         'call':project['CONVOCATORIA'],
#                         'modality':project['MODALIDAD'],
#                         'professor_id':re.search('[0-9]+',project['IDENTIFICACIÓN INVESTIGADOR PRINCIPAL']).group(),
#                         'first_name':first_names,
#                         'last_name':last_names,
#                         'email':project['E-MAIL INVESTIGADOR PRINCIPAL'],
#                         'departament':departaments[project['DEPARTAMENTO O INSTITUTO - INVESTIGADOR PRINCIPAL']],
#                         'faculty':faculty,
#                         'start_date':start_date,
#                         'end_date':end_date,
#                         'total_project':total_resources,
#                         'total_appropriation':s2,
#                         'executed':s,
#                         'total_commitment_balance':total_resources - s,
#                         'execution_percentage':execution_percentage,
#                     }
#                     p = Project.objects.create(**new_project)

#             return True, ''
#         except Exception as e:
#             return False, e