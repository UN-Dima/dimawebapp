import re
from datetime import datetime

import bs4

from projects.models import Project
from groups.models import ResearchGroup
from quipu.models import Resources_QuipuProject, Row_QuipuProject, QuipuProject

from . import nan_2_zero
from .xml_scraper import load_projects_xls, load_report

def save_project(report):
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
                    if type(project['FECHA INICIO']) in [bs4.NavigableString, str]:
                        p.start_date = datetime.strptime(project['FECHA INICIO'].capitalize(), '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
                    else:
                        p.start_date = float('nan')
                    if type(project['FECHA FINAL CON PRÓRROGAS']) == bs4.NavigableString:
                        p.end_date = datetime.strptime(project['FECHA FINAL CON PRÓRROGAS'].capitalize(), '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
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
                    
                    if type(project['FECHA INICIO']) in [bs4.NavigableString, str]:
                        start_date = datetime.strptime(project['FECHA INICIO'].capitalize(), '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
                    else:
                        start_date = float('nan')
                    if type(project['FECHA FINAL CON PRÓRROGAS']) == bs4.NavigableString:
                        end_date = datetime.strptime(project['FECHA FINAL CON PRÓRROGAS'].capitalize(), '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
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
            print(e)
            return False, e

def save_quipu(report):
        """"""

        try:
            for project in report:
                recursos = project.pop('recursos')

                if QuipuProject.objects.filter(pk=project['code']).count():
                    p = QuipuProject.objects.get(pk=project['code'])
                    [recurso.delete() for recurso in p.resources.all()]
                else:
                    p = QuipuProject.objects.create(**project)

                for resource in recursos:

                    recurso = resource.pop('recurso')
                    r = Resources_QuipuProject.objects.create(proyecto=p, resource=recurso)

                    [Row_QuipuProject.objects.create(resource=r, **row) for row in resource['table']]

            return True
        except:
            return False

def save_groups(file):
    
    return False

def update_table(table:str, file:str) -> bool:
    """_summary_

    Parameters
    ----------
    table : str
        Name of the table
         - PROYECTOS
         - QUIPU
         - GRUPOS
    file : str
        Path to the file

    Returns
    -------
    bool
        True if successful, False otherwise
    """

    if table == 'PROYECTOS':
        if file.lower().endswith('.xls'):
            df, report_date = load_projects_xls(open(f'./media_root/{file}','rb'))
            status, msg = save_project(df)
    elif table == 'QUIPU':
        if file.lower().endswith('.xml'):
            status = save_quipu(load_report(open(f'./media_root/{file}','rb')))
    elif table == 'GRUPOS':
        if file.lower().endswith('.xls'):
            status = save_groups(load_report(open(f'./media_root/{file}','rb')))
            
    return status