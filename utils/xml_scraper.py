import bs4
from bs4 import BeautifulSoup as bs
from datetime import datetime
from copy import copy
import re

import urllib.request
import ssl
import numpy as np

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

def load_groups_xls(file_path):
    soup = bs(file_path.read(), "xml")

    data = []
    for d in soup.find_all("Data"):
        if d.contents:
            data += [d.contents[0]]
        else:
            data += [float('nan')]

    data_array = np.array(data)

    s = data_array == 'Registrado'
    s += data_array == 'Categorizado'

    base_url = 'http://www.hermes.unal.edu.co/pages/Consultas/Grupo.jsf?idGrupo='

    groups = []
    for i in np.where(s)[0]:
        group = {'minciencias_code' : data_array[i-4],
                'hermes_code' : data_array[i-7],
                'name' : data_array[i-2],
                'founded' : datetime.strptime(data_array[i+5], '%Y-%m-%dT%H:%M:%S').date(),
                'departament' : data_array[i+9],
                'category' : data_array[i-3],
                'ocde' : f'{data_array[i+3]} | {data_array[i+4]}',
                'leader_id' : data_array[i+6][21:],
                'faculty' : data_array[i+2]}

        try:
            fp = urllib.request.urlopen(base_url+data_array[i-7])
            mybytes = fp.read()

            mystr = mybytes.decode("latin-1")
            fp.close()

            try:
                start = mystr.index('https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=')
                gruplac = mystr[start:]
                end = gruplac.index('target')
                gruplac = gruplac[:end-2]
            except:
                gruplac = float('nan')

            try:
                start = mystr.index('Lineas de investigaci')+137
                end = mystr[start:].index('<a name="enfoque">')-58
                research = mystr[start:start+end].replace('\t','')\
                                                .replace('\n','')\
                                                .replace('&#218;','Ú')\
                                                .replace('&#211;','Ó')\
                                                .replace('&#209;','Ñ')\
                                                .replace('&#205;','Í')\
                                                .replace('&#201;','É')\
                                                .replace('&#193;','Á')\
                                                .split('</li><li>')
            except:
                research = float('nan')

            try:
                start = mystr.index('<div class="informacion-titulo">Agendas de conocimiento </div>')
                end = mystr.index('<div class="informacion-subtitulo">Agendas del conocimiento secundarias</div>')
                knowledge_area = mystr[start+156:end-6].replace('\t','')\
                                                    .replace('\n','')\
                                                    .replace('&#218;','Ú').replace('&#250;','ú')\
                                                    .replace('&#211;','Ó').replace('&#243;','ó')\
                                                    .replace('&#209;','Ñ').replace('&#241;','ñ')\
                                                    .replace('&#205;','Í').replace('&#237;','í')\
                                                    .replace('&#201;','É').replace('&#233;','é')\
                                                    .replace('&#193;','Á').replace('&#225;','á')
            except:
                knowledge_area = float('nan')
        except:
            gruplac = float('nan')
            research = float('nan')
            knowledge_area = float('nan')
        
        group['gruplac'] = gruplac
        group['research'] = research
        group['knowledge_area'] = knowledge_area
        #group['researchers'] = data_array

        groups += [group]
    return groups

def get_members(url):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    members_list = []
    try:
        fp = urllib.request.urlopen(url, context=context)
        mybytes = fp.read()

        mystr = mybytes.decode("latin-1")
        fp.close()

        members = mystr[mystr.index('Integrantes del grupo'):]
        members = members[:members.index('<br/>')]
    except:
        return []
    
    matches = re.findall(r'>([ ]*[A-Za-zÀ-ÿ]+([ ]+[A-Za-zÀ-ÿ]+([ ]+)*([0-9]+)*)+[ ]*)</a>', members, re.UNICODE)
    matches_url = re.findall(r'cod_rh=([0-9]+)', members, re.UNICODE)
    for i in range(len(matches)):
        matches[i] = matches[i][0].replace('  ', ' ')
        matches_url[i] = 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh='+matches_url[i]
        members_list += [[matches[i], matches_url[i]]]
    return members_list

def load_seminars_xls(file_path):
    soup = bs(file_path, "xml")

    data = []
    for d in soup.find_all("Data"):
        if d.contents:
            data += [d.contents[0]]
        else:
            data += [float('nan')]

    data = np.array(data)
    # The first 3 elements are just titles
    # There are 20 headers in all, which we use as our dictionary keys
    headers = data[3:23]

    # Calculate the number of seminars based on the known number of headers
    num_seminars = int(len(data[23:])/20)

    #Make a list of dictionaries
    seminars = []
    for h in data[23:].reshape(num_seminars, 20):
        d = dict(zip(headers, h))
        d['Línea de investigación'] = [d['Línea de investigación']]
        d['Fecha creación'] = datetime.strptime(d['Fecha creación'], '%Y-%m-%dT%H:%M:%S').date()
        seminars += [d]

    # Seminars appear once for every research line.
    # Here we merge all the research lines into one field per seminar
    # We check the last element in the list since seminars are sorted by code
    
    f = [seminars[0]]
    for i in seminars[1:]:
        cod = i['Código']
        if cod == f[-1]['Código']:
            f[-1]['Línea de investigación'] += i['Línea de investigación']
        else:
            f += [i]

    return f