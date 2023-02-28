from django.views.generic.base import TemplateView
from django.http import JsonResponse
from utils.xml_scraper import load_report
from .models import QuipuProject, Row_QuipuProject, Resources_QuipuProject


########################################################################
class QuipuProyectView(TemplateView):

    # ----------------------------------------------------------------------
    def get(self, request, pk=None, *args, **kwargs):
        """"""
        context = self.get_context_data(**kwargs)

        if pk:
            context['project'] = QuipuProject.objects.get(pk=pk)
            context['project_admin'] = QuipuProject._meta
            self.template_name = "proyectos_quipu_view.html"
        else:
            context['projects'] = QuipuProject.objects.all()
            context['projects_admin'] = QuipuProject._meta
            self.template_name = "proyectos_quipu.html"

        return self.render_to_response(context)

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        """"""
        messages = []
        for file in request.FILES.getlist('xmlfile'):
            if file.name.lower().endswith('.xml'):
                if self.save_report(load_report(file)):
                    messages.append(f'Cargado: {file.name}')
                else:
                    messages.append(f'Falló: {file.name}')
            else:
                messages.append(f'Archivo no soportado: {file.name}')

        return JsonResponse({'msg': messages})

    # ----------------------------------------------------------------------
    def save_report(self, report):
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
