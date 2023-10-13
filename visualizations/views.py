from django.shortcuts import render
from django.views.generic.base import TemplateView
import json
# Create your views here.

from groups.models import ResearchGroup
from researchers.models import Professor
from projects.models import Project
from intellectual_property.models import Patent

from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.db.models import Max, Min

import numpy as np
import textwrap
from utils.models import Choices


# ----------------------------------------------------------------------
def break_words(words, width=30, break_='<br>'):
    """"""
    return [break_.join(textwrap.wrap(y_, width=width, break_long_words=False)) for y_ in words]


# ----------------------------------------------------------------------
def fix_filters(model, filters):
    """"""
    #if not filters:
    #    return {}, {}
    searchers = {}
    for k in filters:
        if 'name' in k:
            searchers[k+'__icontains'] = filters[k]
        else:
            k_plain = k.replace('~', '')

            if flts := [c for c in model._meta.get_field(k_plain).choices if filters[k] in c]:
                filters[k] = flts[0][0]

    for k in searchers.keys():
        filters.pop(k[:-11])
    return filters, searchers


########################################################################
class BarsTemplatePlot(TemplateView):
    """"""
    template_name = "empty.html"
    models = {
        'ocde': ResearchGroup,
        'knowledge': ResearchGroup,
        'faculties': ResearchGroup,
        'departament':ResearchGroup,
        'categories': ResearchGroup,
        'researchers_category': Professor,
        'researchers_faculty': Professor,
        'researchers_departament': Professor,
        'researchers_dedication': Professor,
        'projects_faculty': Project,
        'projects_departament': Project,
        'projects_call_type': Project,
        'projects_project_state': Project,
        'projects_total_project': Project,
        'projects_execution_percentage': Project,
        'patent_type': Patent,
        'patent_faculty': Patent,
        'patent_departament': Patent,
    }

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        """"""
        # try:
        context = self.get_context_data(**kwargs)
        data = json.loads(request.POST['data'])
        context.update(data)

        if ctx := data['context']:
            plot = ctx
        else:
            plot = data['id'].split('--')[-1]

        context.update(getattr(self, f'render_{plot}')(
            fix_filters(self.models[plot], data['filters'])[0]))

        if context.get('render_plot', False):
            return self.render_to_response(context)
        else:
            return HttpResponse('')
        # except Exception as e:
            # return HttpResponseNotFound('')

    # ----------------------------------------------------------------------
    def render_ocde(self, filters):
        """"""
        self.template_name = "bars.html"
        if 'category' in filters:
            filters.pop('category')
        x, y = zip(*[(ResearchGroup.objects.filter(ocde=key, **filters).count(), label)
                   for key, label in ResearchGroup._meta.get_field('ocde').choices])
        if sum(x) == 0:
            c1, c2, c3 = [], [], []
        else:
            render_plot = True
            x = np.array(x)
            data = np.array([[s.strip() for s in y_.split('|')] for y_ in y])

            # c1 = data[:, 0][np.argwhere(x != 0)[:, 0]].tolist()
            # c3 = data[:, 2][np.argwhere(x != 0)[:, 0]].tolist()
            y_ = np.array(data[:, 1][np.argwhere(x != 0)[:, 0]].tolist())
            x_ = np.array(x[np.argwhere(x != 0)[:, 0]].tolist())
            percentages = [round(100 * xi / sum(x)) for xi in x]

            x = []
            y = []
            for xi, yi in zip(x_, y_):
                if not yi in y:
                    y.append(yi)
                    x.append(sum(x_[np.argwhere(y_ == yi)[:, 0]]))

            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')
            percentages = [round(100 * xi / sum(x)) for xi in x]

        texttemplate = "%{text}%"
        hovertemplate = "%{x} grupos"

        return locals()

    # ----------------------------------------------------------------------
    def render_knowledge(self, filters):
        """"""
        self.template_name = "bars.html"
        if 'knowledge_area' in filters:
            return {}
        x, y = zip(*[(ResearchGroup.objects.filter(knowledge_area=key, **filters).count(), label)
                   for key, label in ResearchGroup._meta.get_field('knowledge_area').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} grupos"

        return locals()

    # ----------------------------------------------------------------------
    def render_faculties(self, filters):
        """"""
        self.template_name = "Dima Pie.html"
        x, y = zip(*[(ResearchGroup.objects.filter(faculty=key).count(), label)
                   for key, label in ResearchGroup._meta.get_field('faculty').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')
            total_x = sum(x)

        texttemplate = "%{text}%"
        hovertemplate = "%{value} grupos<extra></extra>"
        plottitle = f'{total_x}<br>Grupos'

        return locals()

    # ----------------------------------------------------------------------
    def render_departament(self, filters):
        """"""
        self.template_name = "bars.html"
        if 'departament' in filters:
            return {}
        x, y = zip(*[(ResearchGroup.objects.filter(departament=key, **filters).count(), label)
                   for key, label in ResearchGroup._meta.get_field('departament').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')
            total_x = sum(x)

        texttemplate = "%{text}%"
        hovertemplate = "%{value} grupos"

        return locals()

    # ----------------------------------------------------------------------
    def render_categories(self, filters):
        """"""
        self.template_name = "bars.html"
        if 'category' in filters:
            return {}
        x, y = zip(*[(ResearchGroup.objects.filter(category=key, **filters).count(), label)
                   for key, label in ResearchGroup._meta.get_field('category').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        hovertemplate = "%{value} grupos"
        texttemplate = "%{text}%"

        return locals()

    # ----------------------------------------------------------------------
    def render_researchers_category(self, filters):
        """"""
        self.template_name = "Dima Pie.html"
        x, y = zip(*[(Professor.objects.filter(category=key).count(), label)
                   for key, label in Professor._meta.get_field('category').choices])

        y, x = zip(*[(k, dict(zip(y, x))[k]) for k in Choices.RESEARCHER_CATEGORY_SORTED])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            total_x = sum(x)
            # y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{value} docentes<extra></extra>"
        plottitle = f'{total_x}<br> Docentes'

        return locals()
    # ----------------------------------------------------------------------
    def render_patent_type(self, filters):
        """"""
        if 'patent_type' in filters:
            return {}

        self.template_name = "Dima Pie.html"
        x, y = zip(*[(Patent.objects.filter(patent_type=key).count(), label)
                   for key, label in Patent._meta.get_field('patent_type').choices])

        y, x = zip(*[(k, dict(zip(y, x))[k]) for k in Choices.PATENT_TYPE])
        if sum(x) == 0:
            x, y = [], []
            total_x = 0
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            total_x = sum(x)
            # y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{value} productos<extra></extra>"
        plottitle = f'{total_x}<br> Productos'

        return locals()
    # ----------------------------------------------------------------------
    def render_patent_faculty(self, filters):
        """"""
        if 'faculty' in filters:
            return {}
        if 'departament' in filters:
            return {}

        self.template_name = "bars.html"
        x, y = zip(*[(Patent.objects.filter(faculty=key, **filters).count(), label)
                   for key, label in Patent._meta.get_field('faculty').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} productos"

        return locals()

    # ----------------------------------------------------------------------
    def render_patent_departament(self, filters):
        """"""
        if 'departament' in filters:
            return {}

        self.template_name = "bars.html"
        x, y = zip(*[(Patent.objects.filter(departament=key, **filters).count(), label)
                   for key, label in Patent._meta.get_field('departament').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} productos"
        return locals()
    # ----------------------------------------------------------------------
    def render_researchers_faculty(self, filters):
        """"""
        if 'faculty' in filters:
            return {}
        if 'departament' in filters:
            return {}

        self.template_name = "bars.html"
        x, y = zip(*[(Professor.objects.filter(faculty=key, **filters).count(), label)
                   for key, label in Professor._meta.get_field('faculty').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} docentes"

        return locals()

    # ----------------------------------------------------------------------
    def render_researchers_departament(self, filters):
        """"""
        if 'departament' in filters:
            return {}

        self.template_name = "bars.html"
        x, y = zip(*[(Professor.objects.filter(departament=key, **filters).count(), label)
                   for key, label in Professor._meta.get_field('departament').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} docentes"
        return locals()
    # ----------------------------------------------------------------------
    def render_researchers_dedication(self, filters):
        """"""
        if 'dedication' in filters:
            return {}
        self.template_name = "bars.html"
        x, y = zip(*[(Professor.objects.filter(dedication=key, **filters).count(), label)
                   for key, label in Professor._meta.get_field('dedication').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')
        texttemplate = "%{text}%"
        hovertemplate = "%{x} docentes"
        return locals()
    # ----------------------------------------------------------------------
    def render_projects_faculty(self, filters):
        """"""
        if 'faculty' in filters:
            return {}
        if 'departament' in filters:
            return {}

        self.template_name = "bars.html"
        x, y = zip(*[(Project.objects.filter(faculty=key, **filters).count(), label)
                   for key, label in Project._meta.get_field('faculty').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} proyectos"

        return locals()

    # ----------------------------------------------------------------------
    def render_projects_departament(self, filters):
        """"""
        if 'departament' in filters:
            return {}

        self.template_name = "bars.html"
        x, y = zip(*[(Project.objects.filter(departament=key, **filters).count(), label)
                   for key, label in Project._meta.get_field('departament').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} proyectos"
        return locals()
    # ----------------------------------------------------------------------
    def render_projects_call_type(self, filters):
        """"""
        self.template_name = "Dima Pie.html"
        x, y = zip(*[(Project.objects.filter(call_type=key).count(), label)
                   for key, label in Project._meta.get_field('call_type').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            y = ['Tipologia ' + label for label in y]
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')
            total_x = sum(x)

        texttemplate = "%{text}%"
        hovertemplate = "%{value} proyectos<extra></extra>"
        plottitle = f'{total_x}<br> Proyectos'

        return locals()

    # ----------------------------------------------------------------------
    def render_projects_project_state(self, filters):
        """"""
        if 'project_state' in filters:
            return {}

        self.template_name = "bars.html"
        x, y = zip(*[(Project.objects.filter(project_state=key, **filters).count(), label)
                   for key, label in Project._meta.get_field('project_state').choices])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} proyectos"
        return locals()

    # ----------------------------------------------------------------------
    def render_projects_execution_percentage(self, filters):
        """"""
        #Each element of the list must be a tuple ordered as (values, label)
        ranges = [([0, 0.1], '0-10%'),
                  ([0.1, 0.2], '10-20%'),
                  ([0.2, 0.3], '20-30%'),
                  ([0.3, 0.4], '30-40%'),
                  ([0.4, 0.5], '40-50%'),
                  ([0.5, 0.6], '50-60%'),
                  ([0.6, 0.7], '60-70%'),
                  ([0.7, 0.8], '70-80%'),
                  ([0.8, 0.9], '80-90%'),
                  ([0.9, 1.0], '90-100%'),]
        self.template_name = "bars.html"
        x, y = zip(*[(Project.objects.filter(execution_percentage__range = range, **filters).count(), label)
                   for range, label in ranges])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} proyectos"
        return locals()

    # ----------------------------------------------------------------------
    def render_projects_total_project(self, filters):
        """"""
        bins = 10
        max_value = Project.objects.aggregate(Max('total_project'))['total_project__max']
        min_value = Project.objects.aggregate(Min('total_project'))['total_project__min']
        data_range = max_value - min_value
        delta = data_range/bins
        ranges = [([min_value+delta*i, min_value+delta*(i+1)],
                    f'${(min_value+delta*i)/1e6:.1f}M-${(min_value+delta*(i+1))/1e6:.1f}M')
                    for i in range(bins)] 
        self.template_name = "bars.html"
        x, y = zip(*[(Project.objects.filter(total_project__range = range, **filters).count(), label)
                   for range, label in ranges])
        if sum(x) == 0:
            x, y = [], []
        else:
            render_plot = True
            x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
            percentages = [round(100 * xi / sum(x)) for xi in x]
            y = break_words(y, width = max(map(len, y)) / 2, break_='<br>')

        texttemplate = "%{text}%"
        hovertemplate = "%{x} proyectos"
        return locals()
    # ----------------------------------------------------------------------
    # def render_projects_project_state(self, filters):
    #     """"""
    #     if 'project_state' in filters:
    #         return {}

    #     self.template_name = "bars.html"
    #     x, y = zip(*[(Project.objects.filter(project_state=key, **filters).count(), label)
    #                for key, label in Project._meta.get_field('project_state').choices])
    #     if sum(x) == 0:
    #         x, y = [], []
    #     else:
    #         render_plot = True
    #         x, y = map(list, (zip(*filter(lambda l: l[0], zip(x, y)))))
    #         percentages = [round(100 * xi / sum(x)) for xi in x]
    #         y = break_words(y, width=max(map(len, y)) / 2, break_='<br>')

    #     texttemplate = "%{text}%"
    #     hovertemplate = "%{x} proyectos"
    #     return locals()
########################################################################
class GenerateFilteredOptionsView(View):
    """"""

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        """"""
        data = {}
        filters = json.loads(request.POST['filters'])
        filters = fix_filters(ResearchGroup, filters)

        data['groups'] = [str(g[0]) for g in ResearchGroup.objects.filter(**{k: filters[k]
                                                                             for k in ['faculty', 'departament', 'category'] if k in
                                                                             filters}).values_list('pk')]

        departaments = set([d[0] for d in ResearchGroup.objects.filter(**{k: filters[k]
                                                                          for k in ['faculty'] if k in
                                                                          filters}).values_list('departament')])
        data['departaments'] = [dict(ResearchGroup._meta.get_field(
            'departament').choices)[d] for d in departaments]

        return HttpResponse(json.dumps(data), content_type='text/json')
