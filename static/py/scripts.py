from browser import document, bind, html, window
from dima_scripts import ajax_render, update_plot, ajax_request
import json
import logging

FILTERS_GROUPS = {}
FILTERS_RESEARCHERS = {}
FILTERS_PATENTS = {}
filters = {
    'FILTERS_GROUPS': FILTERS_GROUPS,
    'FILTERS_RESEARCHERS': FILTERS_RESEARCHERS,
    'FILTERS_PATENTS': FILTERS_PATENTS,
}


# ----------------------------------------------------------------------
@bind('#dima-select--category__groups', 'change')
def load_group_view(evt):
    """"""
    global FILTERS_GROUPS
    if evt.target.value == 'All':
        FILTERS_GROUPS.pop('category')
    else:
        FILTERS_GROUPS['category'] = evt.target.value

    update_all_plots(filters_to_use='FILTERS_GROUPS')
    update_all_options(filters_to_use='FILTERS_GROUPS',
                       id='#dima-select--departament__groups')
    ajax_render('dima-render--group', "/grupos/", FILTERS_GROUPS)


# ----------------------------------------------------------------------
@bind('#dima-select--faculty__groups', 'change')
def update_faculty_filter(evt):
    """"""
    global FILTERS_GROUPS

    if evt.target.value == 'All':
        FILTERS_GROUPS.pop('faculty')
    else:
        FILTERS_GROUPS['faculty'] = evt.target.value

    if 'departament' in FILTERS_GROUPS:
        FILTERS_GROUPS.pop('departament')

    document.select_one('#dima-select--departament__groups').value = 'All'

    update_all_plots(filters_to_use='FILTERS_GROUPS')
    update_all_options(filters_to_use='FILTERS_GROUPS',
                       id='#dima-select--departament__groups')
    ajax_render('dima-render--group', "/grupos/", FILTERS_GROUPS)


# ----------------------------------------------------------------------
@bind('#dima-select--departament__groups', 'change')
def update_departament_filter(evt):
    """"""
    global FILTERS_GROUPS
    if evt.target.value == 'All':
        FILTERS_GROUPS.pop('departament')
    else:
        FILTERS_GROUPS['departament'] = evt.target.value
    update_all_plots(filters_to_use='FILTERS_GROUPS')
    # update_all_options(filters_to_use='FILTERS_GROUPS')
    ajax_render('dima-render--group', "/grupos/", FILTERS_GROUPS)


# ----------------------------------------------------------------------
def update_all_plots(filters_to_use):
    """"""
    for element in document.select('.dima-plot'):

        if filters_to_use == element.attrs['filters']:
            update_plot(element.attrs['id'], filters=filters[filters_to_use])


# ----------------------------------------------------------------------
def update_all_options(filters_to_use, id, req=None):
    """"""
    if req is None:
        return ajax_request('options', data={'filters': json.dumps(filters[filters_to_use]), }, callback=lambda evt: update_all_options(filters_to_use, id, evt))

    # Update departaments options
    for option in document.select_one(id).children[1:]:
        if not option.attrs['value'] in req.json['departaments']:
            option.style = {'display': 'none'}
        else:
            option.style = {'display': 'block'}

    # ajax_render('dima-render--group', "/grupos/", filters[filters_to_use])


# # ----------------------------------------------------------------------
# @bind(window, 'load')
# def load_researchers_view(evt):
    # """"""
    # ajax_render('investigadores-tab-pane', "/investigadores/")

    # # document.select_one('#dima-select--faculty__researchers').addEventListener(
        # # "change", update_faculty_filter_)


# ----------------------------------------------------------------------
@bind('#dima-select--faculty__researchers', 'change')
def update_faculty_filter_(evt):
    """"""
    global FILTERS_RESEARCHERS
    if evt.target.value == 'All':
        FILTERS_RESEARCHERS.pop('faculty')
    else:
        FILTERS_RESEARCHERS['faculty'] = evt.target.value

    if 'departament' in FILTERS_RESEARCHERS:
        FILTERS_RESEARCHERS.pop('departament')

    ajax_render('dima-placeholder__researchers',
                "/investigadores/", FILTERS_RESEARCHERS)

    document.select_one(
        '#dima-select--departament__researchers').value = 'All'
    update_all_plots(filters_to_use='FILTERS_RESEARCHERS')
    update_all_options(filters_to_use='FILTERS_RESEARCHERS',
                       id='#dima-select--departament__researchers')


# ----------------------------------------------------------------------
@bind('#dima-select--departament__researchers', 'change')
def update_departament_filter_(evt):
    """"""
    global FILTERS_RESEARCHERS
    if evt.target.value == 'All':
        FILTERS_RESEARCHERS.pop('departament')
    else:
        FILTERS_RESEARCHERS['departament'] = evt.target.value

    ajax_render('dima-placeholder__researchers',
                "/investigadores/", FILTERS_RESEARCHERS)
    update_all_plots(filters_to_use='FILTERS_RESEARCHERS')


# ----------------------------------------------------------------------
@bind('#dima-select--category__researchers', 'change')
def update_researcher_category(evt):
    """"""
    global FILTERS_RESEARCHERS
    if evt.target.value == 'All':
        FILTERS_RESEARCHERS.pop('category')
    else:
        FILTERS_RESEARCHERS['category'] = evt.target.value

    ajax_render('dima-placeholder__researchers',
                "/investigadores/", FILTERS_RESEARCHERS)
    update_all_plots(filters_to_use='FILTERS_RESEARCHERS')


# ----------------------------------------------------------------------
@bind('#dima-select--departament__patents', 'change')
def update_patents_departament(evt):
    """"""
    global FILTERS_PATENTS
    if evt.target.value == 'All':
        FILTERS_PATENTS.pop('departament')
    else:
        FILTERS_PATENTS['departament'] = evt.target.value

    ajax_render('dima-placeholder__patents',
                "/propiedad_intelectual/patents/", FILTERS_PATENTS)


# ----------------------------------------------------------------------
@bind('#dima-select--patent_type__patents', 'change')
def update_patents_types(evt):
    """"""
    global FILTERS_PATENTS
    if evt.target.value == 'All':
        FILTERS_PATENTS.pop('patent_type')
    else:
        FILTERS_PATENTS['patent_type'] = evt.target.value

    ajax_render('dima-placeholder__patents',
                "/propiedad_intelectual/patents/", FILTERS_PATENTS)


# ----------------------------------------------------------------------
@bind('#patentes-tab', 'click')
def update_patentes__plot(evt):
    """"""
    update_all_plots(filters_to_use='FILTERS_PATENTS')
    update_tabs('patentes', 'Propiedad intelectual')


# ----------------------------------------------------------------------
@bind('#investigadores-tab', 'click')
def update_researchers_plot(evt):
    """"""
    update_all_plots(filters_to_use='FILTERS_RESEARCHERS')
    update_tabs('investigadores', 'Investigadores')


# ----------------------------------------------------------------------
@bind('#proyectos-tab', 'click')
def update_proyectos_plot(evt):
    """"""
    update_all_plots(filters_to_use='FILTERS_PATENTS')
    update_tabs('proyectos', 'Proyectos')


# ----------------------------------------------------------------------
@bind('#grupos-tab', 'click')
def update_groups_plot(evt):
    """"""
    update_all_plots(filters_to_use='FILTERS_GROUPS')
    update_tabs('grupos', 'Grupos de investigación')


def update_tabs(tab, breadcrumb):
    """"""

    if not window.location.href.endswith(f'#{tab}'):
        window.location.href = window.location.href[:window.location.href.find('#')] + f'#{tab}'

    document.select_one(
        '.dima-breadcrumb').style = {'display': 'block', }
    document.select_one('.dima-breadcrumb').clear()
    document.select_one(
        '.dima-breadcrumb') <= html.A(breadcrumb, href=f'#{tab}')


# ----------------------------------------------------------------------
@bind(window, 'load')
def on_load(evt):
    """"""
    if window.location.href.endswith('#investigadores'):
        document.select_one('.nav-link#investigadores-tab').click()
        document.select_one(
            '.dima-breadcrumb').style = {'display': 'block', }
        document.select_one(
            '.dima-breadcrumb') <= html.A('Investigadores', href='#investigadores')

    elif window.location.href.endswith('#patentes'):
        document.select_one('.nav-link#patentes-tab').click()
        document.select_one(
            '.dima-breadcrumb').style = {'display': 'block', }
        document.select_one(
            '.dima-breadcrumb') <= html.A('Patentes', href='#patentes')

    else:

        if el := document.select_one('.dima-breadcrumb'):
            el.style = {'display': 'none', }


# ----------------------------------------------------------------------
@bind('.navbar-toggler', 'click')
def navbar_collapse(evt):
    """"""
    navbar = window.bootstrap.Collapse.new(document.select_one("#navbar_content"), {'toggle': False})
    navbar.toggle()


# ----------------------------------------------------------------------
@bind('.btn.btn-default.dropdown-toggle', 'click')
def dropdown_collapse(evt):
    """"""


# ----------------------------------------------------------------------
@bind('.nav-item', 'click')
def nav_item_click(evt):
    """"""
    window.location.href = evt.target.select_one('.nav-link').href


# # ----------------------------------------------------------------------
# @bind('.dima-nav-home li.nav-item', 'mouseover')
# def nav_home_hover(evt):
    # """"""
    # print('XXXX')
    # el = evt.target

    # if color := el.attrs['data-color']:
        # el.style = {
            # 'background-color': color,
        # }

if __name__.startswith('__main__'):
    update_all_plots(filters_to_use='FILTERS_GROUPS')

