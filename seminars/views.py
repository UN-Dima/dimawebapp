from django.views.generic.base import TemplateView
from visualizations.views import fix_filters
from django.http import HttpResponseNotFound
from seminars.models import Seminars
import json


########################################################################
class SeminarView(TemplateView):

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        """"""
        self.template_name = "seminars_table.html"
        context = self.get_context_data(**kwargs)

        filters = fix_filters(
            Seminars, json.loads(request.POST['data']))[0]

        context['seminars'] = Seminars.objects.filter(
            **{k: filters[k]for k in ['faculty', 'departament'] if k in filters})
        context['seminars_admin'] = Seminars._meta

        return self.render_to_response(context)

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        self.template_name = "seminars_view.html"
        context = self.get_context_data(**kwargs)

        try:
            context['seminar'] = Seminars.objects.get(pk=pk)
            context['seminar_admin'] = Seminars._meta
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return self.render_to_response(context)
