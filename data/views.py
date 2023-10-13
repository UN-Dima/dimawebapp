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
from intellectual_property.models import Patent
import os
from datetime import date
from django.http import HttpResponse
import difflib
from django.conf import settings
from visualizations.views import BarsTemplatePlot

########################################################################
class DataView(TemplateView):

    def post(self, request, *args, **kwargs):
        """"""
        self.template_name = "tables.html"

        context = self.get_context_data(**kwargs)
        #choice = json.loads(request.POST['data'])['data_choice']
        #context['data_choice'] = choice

        # context['professors'] = Professor.objects.all()
        # context['professors_admin'] = Professor._meta
        # context['patents_admin'] = Patent._meta
        # context['patents'] = Patent.objects.all()
        # context['projects_admin'] = Project._meta
        # context['projects'] = Project.objects.all()
        # context['groups_admin'] = ResearchGroup._meta
        # context['groups'] = ResearchGroup.objects.all()
        # context['categories'] = Choices.GROUPS_CATEGORY
        # context['faculties'] = Choices.FACULTY
        # context['departaments'] = Choices.DEPARTAMENT
        
        # context['cards'] = [
        #     ('Grupos de investigación', ResearchGroup.objects.count()),
        #     ('Departamentos', len(ResearchGroup._meta.get_field('departament').choices)),
        #     ('Investigadores', Researcher.objects.count() + Professor.objects.exclude(
        #      ** fix_filters(Professor, {'category': 'Sin información', })[0]).count()),
        # ]

        return self.render_to_response(context)

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        self.template_name = "data.html"

        context = self.get_context_data(**kwargs)
        context['OCDE'] = [y for x,y in ResearchGroup._meta.get_field('knowledge_area').choices]
        context['groups'] = ResearchGroup.objects.all()
        context['groups_admin'] = ResearchGroup._meta
        context['faculties'] = Choices.FACULTY
        context['departaments'] = Choices.DEPARTAMENT
        context['categories'] = Choices.GROUPS_CATEGORY
        context['professors'] = Professor.objects.all()
        context['projects'] = Project.objects.all()
        context['patents'] = Patent.objects.all()
        context['projects_admin'] = Project._meta
        context['patents_admin'] = Patent._meta
        context['professors_admin'] = Professor._meta
        context['patent_admin'] = Patent._meta
        context['active_projects'] = Project.objects.filter(project_state='project_state_0001').count()
        context['researcher_categories'] = Choices.RESEARCHER_CATEGORY
        context['patents_types'] = Choices.PATENT_TYPE
        context['call'] = Choices.CALL_TYPE
        context['dedication']=Choices.DEDICATION
        context['type'] = Choices.CALL_TYPE
        context['state'] = Choices.PROJECT_STATE
        context['page'] = 'datos'
        # context['data_choice'] = 'Default'

        return self.render_to_response(context)