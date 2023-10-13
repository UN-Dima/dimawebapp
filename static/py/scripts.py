from browser import document, bind, html, window
from time import sleep
import re
from dima_scripts import ajax_render, update_plot, ajax_request
import json
import logging

FILTERS_GROUPS = {}
FILTERS_RESEARCHERS = {}
FILTERS_PROJECTS = {}
FILTERS_PATENTS = {}
FILTERS_CALLS = {'type':'students', 'title':''}
filters = {
    'FILTERS_GROUPS': FILTERS_GROUPS,
    'FILTERS_RESEARCHERS': FILTERS_RESEARCHERS,
    'FILTERS_PATENTS': FILTERS_PATENTS,
    'FILTERS_PROJECTS': FILTERS_PROJECTS,
    'FILTERS_CALLS': FILTERS_CALLS,
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

    # update_all_options(filters_to_use='FILTERS_GROUPS',
    #                    id='#dima-select--departament__groups')
    ajax_render('dima-render--group', "/grupos/", FILTERS_GROUPS)
    update_all_plots(filters_to_use='FILTERS_GROUPS')

@bind('#dima-select--knowledge__groups', 'change')
def update_knowledge_filter(evt):
    """"""
    global FILTERS_GROUPS
    if evt.target.value == 'All':
        FILTERS_GROUPS.pop('knowledge_area')
    else:
        FILTERS_GROUPS['knowledge_area'] = evt.target.value

    # update_all_options(filters_to_use='FILTERS_GROUPS',
    #                    id='#dima-select--departament__groups')
    ajax_render('dima-render--group', "/grupos/", FILTERS_GROUPS)
    update_all_plots(filters_to_use='FILTERS_GROUPS')

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

    try:
        document.select_one('#dima-select--departament__groups').value = 'All'
        update_all_options(filters_to_use='FILTERS_GROUPS',
                       id='#dima-select--departament__groups')
    except:
        print('No department filter found')
    
    ajax_render('dima-render--group', "/grupos/", FILTERS_GROUPS)
    update_all_plots(filters_to_use='FILTERS_GROUPS')

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

def update_bretheren_style(id, style):
    """"""
    parent = document.select_one(id).parent

    for child in parent.children:
        child.class_name = 'dima-click_buttons dima-click_buttons_inactive'

    document.select_one(id).class_name = 'dima-click_buttons '+style

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

    document.select_one(
        '#dima-select--departament__researchers').value = 'All'
    update_all_plots(filters_to_use='FILTERS_RESEARCHERS')
    update_all_options(filters_to_use='FILTERS_RESEARCHERS',
                       id='#dima-select--departament__researchers')
    ajax_render('dima-render--researchers',
                "/investigadores/", FILTERS_RESEARCHERS)
# ----------------------------------------------------------------------
@bind('#dima-search--first_name__researchers', 'input')
def update_first_name_filter_(evt):
    """"""
    global FILTERS_RESEARCHERS
    if evt.target.value == '':
        FILTERS_RESEARCHERS.pop('first_name')
    else:
        FILTERS_RESEARCHERS['first_name'] = evt.target.value
        FILTERS_RESEARCHERS['last_name'] = evt.target.value

    #update_all_plots(filters_to_use='FILTERS_RESEARCHERS')

    ajax_render('dima-render--researchers',
                "/investigadores/", FILTERS_RESEARCHERS)

# ----------------------------------------------------------------------
@bind('#dima-select--departament__researchers', 'change')
def update_departament_filter_(evt):
    """"""
    global FILTERS_RESEARCHERS
    if evt.target.value == 'All':
        FILTERS_RESEARCHERS.pop('departament')
    else:
        FILTERS_RESEARCHERS['departament'] = evt.target.value

    update_all_plots(filters_to_use='FILTERS_RESEARCHERS')
    ajax_render('dima-render--researchers',
                "/investigadores/", FILTERS_RESEARCHERS)


# ----------------------------------------------------------------------
@bind('#dima-select--category__researchers', 'change')
def update_researcher_category(evt):
    """"""
    global FILTERS_RESEARCHERS
    if evt.target.value == 'All':
        FILTERS_RESEARCHERS.pop('category')
    else:
        FILTERS_RESEARCHERS['category'] = evt.target.value

    update_all_plots(filters_to_use='FILTERS_RESEARCHERS')
    ajax_render('dima-render--researchers',
                "/investigadores/", FILTERS_RESEARCHERS)
# ----------------------------------------------------------------------
@bind('#dima-select--dedication__researchers', 'change')
def update_researcher_dedication(evt):
    """"""
    global FILTERS_RESEARCHERS
    if evt.target.value == 'All':
        FILTERS_RESEARCHERS.pop('dedication')
    else:
        FILTERS_RESEARCHERS['dedication'] = evt.target.value

    update_all_plots(filters_to_use='FILTERS_RESEARCHERS')
    ajax_render('dima-render--researchers',
                "/investigadores/", FILTERS_RESEARCHERS)

# ----------------------------------------------------------------------
@bind('#dima-select--departament__patents', 'change')
def update_patents_departament(evt):
    """"""
    global FILTERS_PATENTS
    if evt.target.value == 'All':
        FILTERS_PATENTS.pop('departament')
    else:
        FILTERS_PATENTS['departament'] = evt.target.value

    ajax_render('dima-render--patents',
                "/propiedad_intelectual/patents/", FILTERS_PATENTS)
    update_all_plots(filters_to_use='FILTERS_PATENTS')
# ----------------------------------------------------------------------
@bind('#dima-select--faculty__patents', 'change')
def update_patents_departament(evt):
    """"""
    global FILTERS_PATENTS
    if evt.target.value == 'All':
        FILTERS_PATENTS.pop('faculty')
    else:
        FILTERS_PATENTS['faculty'] = evt.target.value

    if 'departament' in FILTERS_PATENTS:
        FILTERS_PATENTS.pop('departament')

    document.select_one('#dima-select--departament__patents').value = 'All'
    update_all_options(filters_to_use='FILTERS_RESEARCHERS',
                       id='#dima-select--departament__patents')

    ajax_render('dima-render--patents',
                "/propiedad_intelectual/patents/", FILTERS_PATENTS)
    update_all_plots(filters_to_use='FILTERS_PATENTS')
# ----------------------------------------------------------------------
@bind('#dima-select--patent_type__patents', 'change')
def update_patents_types(evt):
    """"""
    global FILTERS_PATENTS
    if evt.target.value == 'All':
        FILTERS_PATENTS.pop('patent_type')
    else:
        FILTERS_PATENTS['patent_type'] = evt.target.value

    ajax_render('dima-render--patents',
                "/propiedad_intelectual/patents/", FILTERS_PATENTS)
    update_all_plots(filters_to_use='FILTERS_PATENTS')

# ----------------------------------------------------------------------
@bind('#dima-select--call_type__projects', 'change')
def update_project_call_type(evt):
    """"""
    global FILTERS_PROJECTS
    if evt.target.value == 'All':
        FILTERS_PROJECTS.pop('call_type')
    else:
        FILTERS_PROJECTS['call_type'] = evt.target.value

    ajax_render('dima-render--projects',
                "/proyectos/", FILTERS_PROJECTS)

    update_all_plots(filters_to_use='FILTERS_PROJECTS')

# ----------------------------------------------------------------------
@bind('#dima-select--project_state__projects', 'change')
def update_project_project_state(evt):
    """"""
    global FILTERS_PROJECTS
    if evt.target.value == 'All':
        FILTERS_PROJECTS.pop('project_state')
    else:
        FILTERS_PROJECTS['project_state'] = evt.target.value

    update_all_plots(filters_to_use='FILTERS_PROJECTS')
    ajax_render('dima-render--projects',
                "/proyectos/", FILTERS_PROJECTS)

# ----------------------------------------------------------------------
@bind('#dima-select--faculty__projects', 'change')
def update_project_faculty(evt):
    """"""
    global FILTERS_PROJECTS
    if evt.target.value == 'All':
        FILTERS_PROJECTS.pop('faculty')
    else:
        FILTERS_PROJECTS['faculty'] = evt.target.value

    update_all_plots(filters_to_use='FILTERS_PROJECTS')
    ajax_render('dima-render--projects',
                "/proyectos/", FILTERS_PROJECTS)

# ----------------------------------------------------------------------
@bind('#dima-select--departament__projects', 'change')
def update_project_faculty(evt):
    """"""
    global FILTERS_PROJECTS
    if evt.target.value == 'All':
        FILTERS_PROJECTS.pop('departament')
    else:
        FILTERS_PROJECTS['departament'] = evt.target.value

    update_all_plots(filters_to_use='FILTERS_PROJECTS')
    ajax_render('dima-render--projects',
                "/proyectos/", FILTERS_PROJECTS)

@bind('#dima-search--project_name__projects', 'input')
def update_project_name_filter_(evt):
    """"""
    global FILTERS_PROJECTS
    if evt.target.value == '':
        FILTERS_PROJECTS.pop('project_name')
    else:
        FILTERS_PROJECTS['project_name'] = evt.target.value

    ajax_render('dima-render--projects',
                "/proyectos/", FILTERS_PROJECTS)

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
    update_all_plots(filters_to_use='FILTERS_PROJECTS')
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

@bind('#calls_students', 'click')
def update_calls_type(evt):
    """"""
    global FILTERS_CALLS
    FILTERS_CALLS['type'] = 'students'

    update_bretheren_style(id = '#calls_students', style = 'student-title')
    ajax_render('dima-render--calls', '/convocatorias/lista', FILTERS_CALLS)
    
@bind('#calls_inner', 'click')
def update_calls_type(evt):
    """"""
    global FILTERS_CALLS
    FILTERS_CALLS['type'] = 'inner'

    update_bretheren_style(id = '#calls_inner', style = 'inner-title')
    ajax_render('dima-render--calls', '/convocatorias/lista', FILTERS_CALLS)

@bind('#calls_outer', 'click')
def update_calls_type(evt):
    """"""
    global FILTERS_CALLS
    FILTERS_CALLS['type'] = 'outer'

    update_bretheren_style(id = '#calls_outer', style = 'outer-title')
    ajax_render('dima-render--calls', '/convocatorias/lista', FILTERS_CALLS)

@bind('#calls_joint', 'click')
def update_calls_type(evt):
    """"""
    global FILTERS_CALLS
    FILTERS_CALLS['type'] = 'joint'

    update_bretheren_style(id = '#calls_joint', style = 'joint-title')
    ajax_render('dima-render--calls', '/convocatorias/lista', FILTERS_CALLS)

@bind('#calls_minciencias', 'click')
def update_calls_type(evt):
    """"""
    global FILTERS_CALLS
    FILTERS_CALLS['type'] = 'minciencias'

    update_bretheren_style(id = '#calls_minciencias', style = 'minscience-title')
    ajax_render('dima-render--calls', '/convocatorias/lista', FILTERS_CALLS)

@bind('#dima-select--state__calls', 'change')
def update_call_state(evt):
    """"""
    global FILTERS_CALLS
    if evt.target.value == 'All':
        FILTERS_CALLS.pop('state')
    else:
        FILTERS_CALLS['state'] = evt.target.value

    ajax_render('dima-render--calls', '/convocatorias/lista', FILTERS_CALLS)

@bind('#dima-select--student__calls', 'change')
def update_call_student(evt):
    """"""
    global FILTERS_CALLS
    if evt.target.value == 'All':
        FILTERS_CALLS.pop('students')
    else:
        FILTERS_CALLS['students'] = evt.target.value

    ajax_render('dima-render--calls', '/convocatorias/lista', FILTERS_CALLS)

@bind('#dima-search--name__calls', 'input')
def update_first_name_filter_(evt):
    """"""
    global FILTERS_CALLS
    FILTERS_CALLS['title'] = evt.target.value

    ajax_render('dima-render--calls', '/convocatorias/lista', FILTERS_CALLS)

@bind('#dima-select--data', 'change')
def update_data_choice(evt):
    # global FILTERS_DATA
    # FILTERS_DATA['data_choice'] = evt.target.value
    tabs = ['Groups-tab', 'Researchers-tab', 'Patents-tab', 'Projects-tab']
    selection = tabs.pop(tabs.index(evt.target.value)) # remove the selected tab from the list
    for tab in tabs:
        document.select_one(f'#{tab}').style.display = 'none'
    document.select_one(f'#{selection}').style.display = 'inline'

    # Show the plots of the corresponding tab
    # I know python 3.10 has switch statement, but the server is still on 3.9
    if selection == 'Groups-tab':
        update_all_plots(filters_to_use='FILTERS_GROUPS')
    elif selection == 'Researchers-tab':
        update_all_plots(filters_to_use='FILTERS_RESEARCHERS')
    elif selection == 'Patents-tab':
        update_all_plots(filters_to_use='FILTERS_PATENTS')
    else:
        update_all_plots(filters_to_use='FILTERS_PROJECTS')

@bind('#groups-graphs-button1', 'click')
@bind('#groups-graphs-button2', 'click')
@bind('#researchers-graphs-button1', 'click')
@bind('#researchers-graphs-button2', 'click')
@bind('#patents-graphs-button1', 'click')
@bind('#projects-graphs-button1', 'click')
@bind('#projects-graphs-button2', 'click')
def hide_show(evt):
    id = evt.target.id
    state = document.select_one(f'#{id}').class_name.split()
    if state[1] == 'anim-button-open':
        document.select_one(f'#{id}').class_name = 'dima-click_buttons '+'anim-button-closed'
        document.select_one(f'#{id[:-7]}graphs{id[-1]}').style.display = 'none'
    else:                                       
        document.select_one(f'#{id}').class_name = 'dima-click_buttons '+'anim-button-open'
        document.select_one(f'#{id[:-7]}graphs{id[-1]}').style.display = 'flex'

    if 'groups' in id:
        update_all_plots(filters_to_use='FILTERS_GROUPS')
    elif 'researchers' in id:
        update_all_plots(filters_to_use='FILTERS_RESEARCHERS')
    elif 'patents' in id:
        update_all_plots(filters_to_use='FILTERS_PATENTS')
    else:
        update_all_plots(filters_to_use='FILTERS_PROJECTS')

@bind("#executed", "keyup")
@bind("#total_project", "keyup")
@bind("#source_1", "keyup")
def monetize(event):
    id = event.target.id
    value = document[id].value
    value = re.subn('[^0-9]','',value)[0]
    value = [value[::-1][i:i+3] for i in range(0, len(value), 3)]
    document[id].value = f'${".".join(value)[::-1]}'

@bind("#add_source--1", "click")
def add_source(evt):
    parent = document.select_one(f'#source_1').parent
    i = 2
    while document.select_one(f'#source_{i}'):
        i += 1
    label = html.LABEL(**{"for":f"source_{i}"}) 
    label <= html.B(f'Desembolso #{i}')
    parent <= label + html.BR()
    parent <= html.INPUT(type="text", name=f"source_{i}", id=f"source_{i}") + html.BR()
    parent.children[-2].bind("keyup", monetize)
    
@bind("#remove_source--1", "click")
def remove_source(evt):
    parent = document.select_one(f'#source_1').parent
    i = 2
    while document.select_one(f'#source_{i}'):
        i += 1
    i -= 1
    if i>1:
        children = parent.children
        index = children.index(document.select_one(f'#source_{i}'))
        children[index+1].remove() # <br>
        children[index].remove() # <input>
        children[index-1].remove() # <br>
        children[index-2].remove() # <label>

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

