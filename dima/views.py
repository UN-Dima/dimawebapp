from django.views.generic.base import TemplateView
# Create your views here.
from utils.models import Choices
from groups.models import ResearchGroup
from django.shortcuts import render
from researchers.models import Researcher, Professor
from projects.models import Project
import json
import numpy as np
from visualizations.views import fix_filters
from django.http import HttpResponseNotFound
from .models import Newsletter, Broadcast, Team, Content
from intellectual_property.models import Patent
import os
from datetime import date
from django.http import HttpResponse
import difflib
from django.conf import settings

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
def buscar_resultados_similares(lista, palabra):
    posiciones_similares = []
    coincidencias = difflib.get_close_matches(palabra, lista, n=6, cutoff=0.5)
    
    for coincidencia in coincidencias:
        posiciones = [i for i, elem in enumerate(lista) if elem == coincidencia]
        posiciones_similares.extend(posiciones)
    
    return posiciones_similares

class ContentView(TemplateView):
    label=''
    def post(self, request, **kwargs):
        context=self.get_context_data()
        folder=request.POST.get('folder')
        filter=request.POST.get('q')
        files=[]
        for attachment in Content.objects.get(label=self.label).attachment.all():
            if attachment.label =='file' and attachment.area == folder:
                files.append([attachment.name,attachment.area,attachment.type,attachment.attachment])       
        if folder:
            context['file_data']=folder
            context['files']=files
            return render(request,'static/content_view.html',context)
        elif filter:
            files=[]
            for attachment in Content.objects.get(label=self.label).attachment.all():
                if attachment.label =='file':
                    files.append([attachment.name,attachment.area,attachment.type,attachment.attachment])
            result = buscar_resultados_similares(np.array(files)[:,0], filter)
            

            context['filter']=filter
            context['files']=np.array(files)[result,:]
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
        
        return context
