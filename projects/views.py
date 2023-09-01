from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Project
from researchers.models import Professor
from utils.models import Choices
from visualizations.views import fix_filters
from django.http import HttpResponseNotFound
import json
from django.db.models import Q

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