from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Professor
from utils.models import Choices
from visualizations.views import fix_filters
from django.http import HttpResponseNotFound
import json
from django.db.models import Q

########################################################################
class Researchers(TemplateView):

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        """"""
        self.template_name = "researchers_list.html"
        context = self.get_context_data(**kwargs)

        filters, searchers = fix_filters(
            Professor, json.loads(request.POST['data']))
        print(json.loads(request.POST['data']))
        query = Q()
        if 'first_name__icontains' in searchers:
            query |= Q(first_name__icontains=searchers['first_name__icontains'])
        if 'last_name__icontains' in searchers:
            query |= Q(last_name__icontains=searchers['last_name__icontains'])

        professors = Professor.objects.filter(
        query,
        **{k: filters[k] for k in ['faculty', 'departament', 'category', 'dedication'] if k in filters}
        )

        context['professors'] = professors
        context['professors_admin'] = Professor._meta
        return self.render_to_response(context)

    # ----------------------------------------------------------------------
    def get(self, request, obscure=None, *args, **kwargs):
        """"""
        self.template_name = "researchers_view.html"
        context = self.get_context_data(**kwargs)

        try:
            context['professor'] = Professor.objects.get(pk=Professor.unobscure(obscure))
            context['professor_admin'] = Professor._meta
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return self.render_to_response(context)
