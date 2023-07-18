from django.views.generic.base import TemplateView
# Create your views here.
from utils.models import Choices
from groups.models import ResearchGroup
from django.shortcuts import render
from researchers.models import Researcher, Professor
from projects.models import Project
import json
from visualizations.views import fix_filters
from django.http import HttpResponseNotFound
from .models import Newsletter, Broadcast, Team, Content
from intellectual_property.models import Patent
import os
from datetime import date
from django.http import HttpResponse
import difflib

########################################################################
class HomeView(TemplateView):
    template_name = "home.html"

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)
        context['broadcasts'] = Broadcast.objects.filter(expiration__gt=date.today())
        context['broadcasts_admin'] = Broadcast._meta
        return context


########################################################################
class DataView(TemplateView):
    template_name = "data.html"

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)
        context['OCDE'] = Choices.OCDE
        context['groups'] = ResearchGroup.objects.all()
        context['groups_admin'] = ResearchGroup._meta
        # context['broadcasts'] = Broadcast.objects.filter(
            # expiration__gt=date.today())
        # context['broadcasts_admin'] = Broadcast._meta
        context['faculties'] = Choices.FACULTY
        context['departaments'] = Choices.DEPARTAMENT
        context['categories'] = Choices.GROUPS_CATEGORY
        context['professors'] = Professor.objects.all()
        context['projects'] = Project.objects.all()
        context['patents'] = Patent.objects.all()
        context['patents_admin'] = Patent._meta
        context['professors_admin'] = Professor._meta
        context['researcher_categories'] = Choices.RESEARCHER_CATEGORY
        context['patents_types'] = Choices.PATENT_TYPE
        context['patent_admin'] = Patent._meta
        context['dedication']=Choices.DEDICATION
        context['type'] = Choices.CALL_TYPE
        context['state'] = Choices.PROJECT_STATE
        context['page'] = 'datos'


        context['cards'] = [
            ('Grupos de investigación', ResearchGroup.objects.count()),
            ('Departamentos', len(ResearchGroup._meta.get_field('departament').choices)),
            ('Investigadores', Researcher.objects.count() + Professor.objects.exclude(
             ** fix_filters(Professor, {'category': 'Sin información', })[0]).count()),
        ]

        return context


########################################################################
class NewsletterView(TemplateView):
    template_name = "newsletter.html"

    # ----------------------------------------------------------------------

    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)
        context['newsletters'] = Newsletter.objects.all()
        context['newsletters_admin'] = Newsletter._meta
        context['page'] = 'boletines'
        return context


########################################################################
class TeamView(TemplateView):
    template_name = "static/equipo_de_trabajo.html"

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        context['teams_admin'] = Team._meta
        context['page'] = 'contacto'
        return context


########################################################################
def tamano_carpeta(carpeta):
    tamano_total = 0

    for ruta_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(ruta_actual, archivo)
            tamano_total += os.path.getsize(ruta_completa)
    tamano_mb = tamano_total / (1024 * 1024)
    return round(tamano_mb,2)
def buscar_resultados_similares(diccionario, palabra):
    resultados_similares = {}
    for clave, valores in diccionario.items():
        coincidencias = difflib.get_close_matches(palabra, valores, n=6, cutoff=0.5)
        if coincidencias:
            resultados_similares[clave] = coincidencias
    return resultados_similares
class ContentView(TemplateView):
    label=''
    def post(self, request, **kwargs):
        context=self.get_context_data()
        folder=request.POST.get('folder')
        filter=request.POST.get('q')
        path = 'media_root/uploads/content/'
        folder_path = 'media/uploads/content/'
        if folder:

            files_root={}
            files=os.listdir(path+folder+'/')
            aux=[]
            for file in files:
                s=file.split('.')
                aux.append([s[0],folder_path+folder+"/"+file,s[1],self.Area[folder.replace(' ','_')]])

            files_root[folder]=aux
            context['file_data']=files_root
            return render(request,'static/content_view.html',context)
        elif filter:
            result = buscar_resultados_similares(self.file_filter, filter)
            file_result={}
            for key,values in result.items():
                aux=[]
                for value in values:
                    s=value.split('.')
                    aux.append([s[0],folder_path+key+"/"+value,s[1],self.Area[key.replace(' ','_')]])
                file_result[key]=aux
            context['file_data']=file_result
            return render(request,'static/formatos.html',context)
        
    
        
    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        
        """"""
        context = super().get_context_data(**kwargs)
        context[self.label] = Content.objects.get(label=self.label)
        context[f'{self.label}_admin'] = Content._meta

        if self.label == 'home':
            context['broadcasts'] = Broadcast.objects.filter(expiration__gt=date.today())
            context['broadcasts_admin'] = Broadcast._meta
            context['page'] = 'home'
        # Obtener la lista de archivos en una ubicación específica
        self.file_filter={}
        
        folder_root={}
        path = 'media_root/uploads/content/'
        folders = os.listdir(path)
        self.Area={'Comité_de_ética':'Comité de ética','Certificado_estudiantes':'Estudiante auxiliar',
         'Formatos_contrapartidas':'Contrapartidas','Gestión_propiedad_intelectual':'Propiedad_intelectual',
         'Marketing_tecnológico':'Lorem impsum','Paz_y_salvos':'Paz y salvo','Solicitudes':'Solicitudes'}
        zip_path = 'media_root/uploads/Zip/'
        zip_path_m='media/uploads/Zip/'
        url=[zip_path_m+i for i in os.listdir(zip_path)]
        for j,u in zip(folders,url):
            self.file_filter[j]=os.listdir(path+j+'/')
            folder_root[j]=[tamano_carpeta(path+j+'/'),self.Area[j.replace(' ','_')],u]
        aux=['Certificado estudiantes', 'Comité de ética']
        folder_path = 'media/uploads/content/'
        files_root={}
        
        for folder in aux:
            aux=[]
            files=os.listdir(path+folder+'/')
            for file in files:
                s=file.split('.')
                aux.append([s[0],folder_path+folder+"/"+file,s[1]])

            files_root[folder]=aux
        
        context['file_view']=files_root
        #for i,j in 
        #os.listdir(path+)
        context['folder_data'] = folder_root

        return context
