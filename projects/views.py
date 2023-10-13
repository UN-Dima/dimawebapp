#Python Natives
import io
import json
import re

#3rd Party libraries
from django.http import FileResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseNotFound
from django.db.models import Q

#Local Libraries
from .models import Project
from researchers.models import Professor
from utils.models import Choices
from utils.pdfgen import project_template
from visualizations.views import fix_filters

########################################################################
class Projects(TemplateView):

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        """"""
        self.template_name = "projects_list.html"
        context = self.get_context_data(**kwargs)

        filters, searchers = fix_filters(
            Project, json.loads(request.POST['data']))

        query = Q()

        if 'project_name__icontains' in searchers:
            query |= Q(project_name__icontains=searchers['project_name__icontains'])

        projects = Project.objects.filter(
            query,
            **{k: filters[k] for k in ['faculty', 'departament', 'type', 'call_type', 'project_state'] if k in filters}
        )

        context['projects'] = projects
        context['projects_admin'] = Project._meta

        
        return self.render_to_response(context)
        

    # ----------------------------------------------------------------------
    def get(self, request, obscure=None, *args, **kwargs):
        """"""
        self.template_name = "projects_view.html"
        context = self.get_context_data(**kwargs)

        try:
            context['project'] = Project.objects.get(pk=Project.unobscure(obscure))
            context['project_admin'] = Project._meta
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return self.render_to_response(context)

########################################################################
class Project_Report(TemplateView):

    # ----------------------------------------------------------------------
    def post(self, request, obscure=None, *args, **kwargs):
        """"""
        context = self.get_context_data(**kwargs)

        try:
            context['project'] = Project.objects.get(pk=Project.unobscure(obscure))
            context['project_admin'] = Project._meta
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        
        return self.render_to_response(context)
        

    # ----------------------------------------------------------------------
    def get(self, request, obscure=None, *args, **kwargs):
        """"""
        self.template_name = "projects_report.html"
        context = self.get_context_data(**kwargs)

        try:
            context['project'] = Project.objects.get(pk=Project.unobscure(obscure))
            context['project_admin'] = Project._meta
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return self.render_to_response(context)

########################################################################
def project_report(request, obscure=None, *args, **kwargs):
        """"""
        items = ['project_name', 'start_date', 'end_date',
                 'hermes_cod', 'quipu_cod_0',
                 'call', 'researcher', 'total_project',
                 'executed', 'note']
        info = {}

        for key, value in request.GET.items():
            info[key] = value

        info['executed'] = re.subn('[^0-9]', '', info['executed'])[0]
        info['total_project'] = re.subn('[^0-9]', '', info['total_project'])[0]
        info['total_commitment_balance'] = int(info['total_project']) - int(info['executed'])

        project = Project.objects.get(pk=Project.unobscure(obscure))
        buffer = io.BytesIO()

        project_template(buffer, info)


        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="Reporte.pdf")