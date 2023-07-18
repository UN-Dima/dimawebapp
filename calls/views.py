from django.views.generic.base import TemplateView
from .models import InternalCall, JointCall, MincienciasCall, StudentsCall
from utils.models import Choices
import json

def calls_filter(database, filters):
    """This is a temporary function to filter using the calls database. Since some filters
    are based on python properties, this function checks this property for the entire database.

    THIS FUNCTION IS NOT VIABLE TO LARGER DATABSES, IT IS ONLY MEANT TO BE A TEMPORARY FIX

    Parameters
    ----------
    database : Django.Model
        The Django database model.
    filters : dict
        The python dictionary containing the list of filters.

    Returns
    -------
    list
        List of objects matching the filters
    """
    filtered = list(database)
    reset = True
    for key, value in filters.items():
        if reset:
            reset = False
            if key == 'state' and value == 'Abierta':
                filtered = [x for x in database if not x.expired]
            if key == 'state' and value == 'Finalizada':    
                filtered = [x for x in database if x.expired]
            if key == 'students' and value == 'Posgrado':
                filtered = [x for x in database if x.postgraduate]
            if key == 'students' and value == 'Pregrado':
                filtered = [x for x in database if x.undergraduate]
        else:
            if key == 'state' and value == 'Abierta':
                filtered = [x for x in filtered if not x.expired]
            if key == 'state' and value == 'Finalizada':    
                filtered = [x for x in filtered if x.expired]
            if key == 'students' and value == 'Posgrado':
                filtered = [x for x in filtered if x.postgraduate]
            if key == 'students' and value == 'Pregrado':
                filtered = [x for x in filtered if x.undergraduate]
    return filtered

########################################################################
class CallsView(TemplateView):
    def post(self, request, *args, **kwargs):
        self.template_name = "convocatorias/calls_list.html"
        filters = json.loads(request.POST['data'])
        call_type = filters.pop('type')
        call_title = filters.pop('title')
        context = self.get_context_data(**kwargs)

        if call_type == 'students':
            context['calls'] = calls_filter(StudentsCall.objects.filter(title__icontains=call_title).order_by('-expiration'),filters)
            context['calls_admin'] = StudentsCall._meta
        elif call_type == 'inner':
            context['calls'] = InternalCall.objects.filter(title__icontains=call_title).order_by('-expiration')
            context['calls_admin'] = InternalCall._meta
        elif call_type == 'outer':
            context['calls'] = MincienciasCall.objects.filter(title__icontains=call_title).order_by('-expiration')
            context['calls_admin'] = MincienciasCall._meta
        elif call_type == 'joint':
            context['calls'] = JointCall.objects.filter(title__icontains=call_title).order_by('-expiration')
            context['calls_admin'] = JointCall._meta
        elif call_type == 'minciencias':
            context['calls'] = MincienciasCall.objects.filter(title__icontains=call_title).order_by('-expiration')
            context['calls_admin'] = MincienciasCall._meta

        context['call_type'] = call_type
        return self.render_to_response(context)

    def get(self, request, pk=None, *args, **kwargs):
        self.template_name = "convocatorias/convocatorias.html"
        context = self.get_context_data(**kwargs)
        context['page'] = 'convocatorias'

        context['call_type'] = 'students'
        context['calls'] = StudentsCall.objects.all().order_by('-expiration')
        context['calls_admin'] = StudentsCall._meta

        context['call_state'] = Choices.CALL_STATE
        context['call_student'] = Choices.CALL_STUDENT

        return self.render_to_response(context)

########################################################################
class InternalCallView(TemplateView):

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        context = self.get_context_data(**kwargs)
        context['page'] = 'convocatorias'

        if pk:
            self.template_name = "convocatorias/internas_view.html"
            context['internalcall'] = InternalCall.objects.get(pk=pk)
            context['internalcall_admin'] = InternalCall._meta
        else:
            self.template_name = "convocatorias/internas.html"
            context['internalcall'] = InternalCall.objects.all()
            context['internalcall_admin'] = InternalCall._meta

        return self.render_to_response(context)


########################################################################
class JointCallView(TemplateView):

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        context = self.get_context_data(**kwargs)
        context['page'] = 'convocatorias'

        if pk:
            self.template_name = "convocatorias/conjunta_view.html"
            context['jointcall'] = JointCall.objects.get(pk=pk)
            context['jointcall_admin'] = JointCall._meta
        else:
            self.template_name = "convocatorias/conjuntas.html"
            context['jointcall'] = JointCall.objects.all()
            context['jointcall_admin'] = JointCall._meta

        return self.render_to_response(context)


########################################################################
class MincienciasCallView(TemplateView):

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        context = self.get_context_data(**kwargs)
        context['page'] = 'convocatorias'

        if pk:
            self.template_name = "convocatorias/minciencias_view.html"
            context['mincienciascall'] = MincienciasCall.objects.get(pk=pk)
            context['mincienciascall_admin'] = MincienciasCall._meta
        else:
            self.template_name = "convocatorias/minciencias.html"
            context['mincienciascall'] = MincienciasCall.objects.all()
            context['mincienciascall_admin'] = MincienciasCall._meta

        return self.render_to_response(context)


########################################################################
class StudentsCallView(TemplateView):

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        context = self.get_context_data(**kwargs)
        context['page'] = 'convocatorias'

        if pk:
            self.template_name = "convocatorias/estudiantes_view.html"
            context['studentscall'] = StudentsCall.objects.get(pk=pk)
            context['studentscall_admin'] = StudentsCall._meta
        else:
            self.template_name = "convocatorias/estudiantes.html"
            context['studentscall'] = StudentsCall.objects.all().order_by('-expiration')
            context['studentscall_admin'] = StudentsCall._meta

        return self.render_to_response(context)
