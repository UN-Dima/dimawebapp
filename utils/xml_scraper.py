import bs4
from bs4 import BeautifulSoup as bs
from datetime import datetime
from copy import copy

REINDEX = {
    'IMPUTACION': 'imputacion',
    'APROPIACION_DEFINITIVA': 'apropiacion',
    'DISPONIBILIDAD': 'disponibilidad',
    'REGISTRO': 'registro',
    'OBLIGACIONES': 'obligaciones',
    'PAGO': 'pago',
    'SALDO_DISPONIBLE': 'cupo',
    'SALDO_DISPONIBLE2': 'saldo_por_comprometer',
    'CF_1': 'por_ejecutar',
}


def childs(element: bs4.element) -> int:
    """Return the count of childrens for element without destroying the generator."""
    return len(list(copy(element).children))


def walk(children: list[bs4.element]) -> list[bs4.element]:
    d = []
    for element in children:
        if name := element.name:
            if childs(element) == 1:
                pass
                # print(f'{name}: {element.text}')
            else:
                d.append(copy(element))
    if len(d) == 1:
        return d[0]
    else:
        return d


def load_report(file_path):

    data = bs(file_path.read(), 'xml')

    out = {}

    desc, data_l1 = data.children

    out['inicio_reporte'] = datetime.strptime(data_l1.find('CF_DESDE').text, '%Y%m')
    out['fin_reporte'] = datetime.strptime(data_l1.find('CF_HASTA').text, '%Y%m')

    data_l2 = walk(data_l1.children)
    data_l3 = walk(data_l2.children)
    data_l4 = walk(data_l3.children)

    out['empresa'] = data_l3.find('MOVI_CIAS').text

    data_l4 = walk(data_l3.children)
    data_l5 = walk(data_l4.children)

    report = []
    for prj in data_l5:
        data_prj = walk(prj)
        project = {**out}
        code, proyecto = prj.find('AREA_DESCRI').text.split('-', 1)
        project['code'] = code
        project['proyecto'] = proyecto.strip()

        project['recursos'] = []

        if not data_prj:
            continue

        for rec in data_prj.find_all('G_RECU'):
            recurso = {}
            recurso['recurso'] = rec.find('MOVI_RECU').text

            data_prj = walk(rec)
            data_prj = walk(data_prj)
            data_prj = walk(data_prj)
            recurso['table'] = [{REINDEX[k]:row.find(k).text for k in REINDEX} for row in data_prj]

            project['recursos'].append(recurso.copy())

        report.append(project)
    return report


def load_projects_xls(file_path):
    # Create a 'soup' object.
    # Hermes currently generates xls files using xml format.
    # This means although programs like excel can open the files
    # they should be treated like xmls to prevent data loss.
    soup = bs(file_path.read(), "xml")

    # We create a 'data' list
    # Think like each entry on this list is a cell in order from
    # top-left to bottom-right, with empty cells in between being
    # set to NaN.
    data = []
    for d in soup.find_all("Data"):
        if d.contents:
            data += [d.contents[0]]
        else:
            data += [float("nan")]

    # The last cell has the report's date.
    # The row has a mixture of text and date, so I manually get rid of the text.
    # This should be done with regex in the future
    date = data[-1][19:-16]
    date = datetime.strptime(date, '%b %d, %Y %I:%M %p').strftime('%d/%b/%Y')
    
    # This assumes the table was generated with all the information available.
    # I am also assuming the "research group" column is being included.
    # In total we should have 37 columns per project.
    headers = data[3:40] 

    # The last cell has the date which we already extracted.
    # The cell before that is empty for padding.
    # Aside from that: project_info = data - headers
    project_info = data[40:-2]

    # We'll make a list of dictionaries so it's easy for tools like pandas to create headers
    # later on.
    df = []

    # num_projects = project_info/num_headers
    for i in range(int(len(project_info)/37)):
        # Create an empty dictionary
        entry = {}
        # For each header we include the corresponding info.
        # Since we read the data as a list, it should be in the same order
        # as headers.
        for h,dat in zip(headers, project_info[i*37:(i+1)*37]):
            entry[h] = dat
        # Add the dictionary to the list
        df += [entry]

    return df, date