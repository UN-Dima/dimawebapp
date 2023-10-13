#Python Natives
from datetime import date, timedelta, datetime

#3rd Party libraries
from django.contrib.humanize.templatetags.humanize import intcomma
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.colors import HexColor

#Local Libraries
from dima.models import Team

def none_to_zero(x):
    """Just a function for prototyping to deal with None objects

    Parameters
    ----------
    x : None, other
        A variable

    Returns
    -------
    1, x
        if x is None, then it returns 1, else returns x
    """
    if x == None: return 1
    else: return x

def draw_title(canvas, msg, x, y, max_width, max_height):
    """Draw a title paragraph

    Parameters
    ----------
    canvas : reportlab.canvas.Canvas object
        The canvas on which the title will be written on. The Canvas object "file"
        should be a io.BytesIO object.
    msg : str
        The title paragraph
    x : int
        x-cordinate for the textbox.
        Please remember reportlab uses the lower left corner as the origin.
    y : int
        y-cordinate for the textbox.
        Please remember reportlab uses the lower left corner as the origin.
    max_width : int
        The textbox's width. If the text surpasses this value, then it wraps
        to the next line.
    max_height : int
        The textbox's height. If the text surpasses this value, then it disappears.

    Returns
    -------
    w : int
        The final width of the textbox after adjusting the text.
    h : int
        The final height of the textbox after adjusting the text.
    """
    message_style = ParagraphStyle('bold', alignment = 1, fontSize = 10, leading=15, fontName='Helvetica')
    message = msg.replace('\n', '<br />')
    message = Paragraph(message, style=message_style)
    w, h = message.wrap(max_width, max_height)
    message.drawOn(canvas, x, y - h)
    return w, h

def draw_text(canvas, msg, x, y, max_width, max_height):
    """Draw a normal paragraph

    Parameters
    ----------
    canvas : reportlab.canvas.Canvas object
        The canvas on which the title will be written on. The Canvas object "file"
        should be a io.BytesIO object.
    msg : str
        The paragraph
    x : int
        x-cordinate for the textbox.
        Please remember reportlab uses the lower left corner as the origin.
    y : int
        y-cordinate for the textbox.
        Please remember reportlab uses the lower left corner as the origin.
    max_width : int
        The textbox's width. If the text surpasses this value, then it wraps
        to the next line.
    max_height : int
        The textbox's height. If the text surpasses this value, then it disappears.

    Returns
    -------
    w : int
        The final width of the textbox after adjusting the text.
    h : int
        The final height of the textbox after adjusting the text.
    """
    message_style = ParagraphStyle('Normal', alignment = 0, fontSize = 10, leading=12, fontName='Helvetica')
    message = msg.replace('\n', '<br />')
    message = Paragraph(message, style=message_style)
    w, h = message.wrap(max_width, max_height)
    message.drawOn(canvas, x, y - h)
    return w, h

def project_template(buffer, info, ):
    """
    This function takes an io.BytesIO buffer to create a pdf based on the information 
    in model. model should already be the specific project you wish to use.

    Parameters
    ----------
    buffer : io.BytesIO object
        The request buffer to download the pdf.
    info : dict
        A dictionary with the report information
    """
    today = date.today()
    start = datetime.strptime(info['start_date'], "%Y-%m-%d").date()
    end = datetime.strptime(info['end_date'], "%Y-%m-%d").date()
    if end == start:
        end += timedelta(days=36525)
    signee = Team.objects.get(area='Apoyo Hermes para la sede Manizales')
    time_budget = end - start
    c = canvas.Canvas(buffer, pagesize = letter)  # letter pagesize

    c.drawImage('./static/assets/dima_logo_blue.png', x = 88, y= 676, width=83, height=21)

    leading = 12
    items = ['CÓDIGO PROYECTO:',
            'CÓDIGO QUIPU:',
            'NOMBRE PROYECTO:',
            'CONVOCATORIA:',
            'DOCENTE:',
            'FECHA DE INICIO:',
            'FECHA DE FINALIZACIÓN:',
            'PRESUPUESTO TOTAL:',
            'DESEMBOLSO #1:',]

    information = [f'{info["hermes_cod"]}',
            f'{info["quipu_cod_0"]}', #Project can have more than 1 quipu code
            f'{info["project_name"]}',
            f'{info["call"]}',
            f'{info["researcher"]}',
            f'{start.strftime("%d/%m/%Y")}',
            f'{end.strftime("%d/%m/%Y")}',
            f'${intcomma(info["total_project"])}',
            f'{intcomma(info["source_1"])}',]

    keys = info.keys()
    i = 2
    while f"source_{i}" in keys:
        items += [f'DESEMBOLSO #{i}:']
        information += [f'{intcomma(info[f"source_{i}"])}']
        i += 1
    items += ['PRESUPUESTO EJECUTADO:',
            'PRESUPUESTO POR\nCOMPROMETER:',]
    information += [f'${intcomma(info["executed"])}',
                    f'${intcomma(info["total_commitment_balance"])}',]


    #La Nota depende del proyecto
    para = [f'Estimado docente, a la fecha el tiempo de ejecución de su proyecto es de {str(today - start)[:-14]} días, que corresponden al {(today - start)/time_budget*100:.2f}% del tiempo total.',
    f'En cuanto al presupuesto, se le informa que a la fecha se ha ejecutado el {int(info["executed"])/int(info["total_project"])*100:.2f}% del total aprobado, por lo que se recomienda ejecutar el presupuesto disponible antes de que se cumpla el plazo establecido para el desarrollo del proyecto.',]

    if info['note']:
        note = '<b>Nota</b> '+info['note']+'\n\n\n'
    else:
        note = ''
        
    signature = f'Cordialmente,\n\n{signee.names}\n{signee.area}\nSede Manizales\n<a href="mailto:{signee.email}" color="blue"><u>{signee.email}</u></a>'

    w, h = draw_title(c, '<b>UNIVERSIDAD NACIONAL DE COLOMBIA SEDE MANIZALES\nDIRECCIÓN DE INVESTIGACIÓN Y EXTENSIÓN\nFORMATO DE SEGUIMIENTO</b>', x = 228, y = 720,
                max_width = 300, max_height = 300)
                
    x, y = 90, 720

    y = y - h - leading - 3

    draw_text(c, 'FECHA DE CORTE:', x, y, max_width = 200, max_height = 200)
    w, h = draw_text(c,today.strftime('%d/%m/%Y'), x + 150, y, 345, 500)

    for i in range(len(items)):
        #Move cursor into position
        y = y - h - leading
        #Check if there is enough room for the next paragraph
        if y <= 70:
            c.showPage()
            y = 720
        draw_text(c, items[i], x, y, max_width = 200, max_height = 200)
        w, h = draw_text(c, information[i], x + 150, y, 345, 500)

    x = 88
    y -= 15

    for i in range(2):
        #Move cursor into position
        y = y - h - leading
        #Check if there is enough room for the next paragraph
        if y <= 70:
            c.showPage()
            y = 720
        w, h = draw_text(c, para[i], x, y, 500, 500)

    # Check if there is enough room for the graphics
    if y <= 220:
        c.showPage()
        y = 720

    y -= 50
    draw_text(c, 'Tiempo', x+92, y, 200, 500)
    draw_text(c, 'Presupuesto', x+320, y, 200, 500)

    # Pie Chart
    y -= 100 # chart_height

    d = Drawing(width = 200, height = 100)

    pc = Pie()
    pc.slices.fontName = 'Helvetica'
    pc.x = 30
    pc.data = [(today - start)/time_budget*100, 100-(today - start)/time_budget*100,]
    pc.labels = [f'{x:.2f}%' for x in pc.data]
    pc.slices.labelRadius = 0.7

    colors = [HexColor('#5b9bd5'), HexColor('#70ad47'),]
    for i, color in enumerate(colors): 
        pc.slices[i].fillColor =  color

    pc.slices.strokeWidth = 0.1
    pc.slices.strokeColor = colors[0]

    legend = Legend()
    legend.fontName='Helvetica'
    legend.alignment = 'right'
    legend.columnMaximum = 1
    legend.y = -10
    legend.colorNamePairs = [(x,y) for x,y in zip(colors,['Tiempo Ejecutado', 'Tiempo Restante'])]

    d.add(legend)
    d.add(pc)

    d.drawOn(c, x+30, y - 20) # y-cordinate doesn't quite align so we need some extra padding

    d2 = Drawing(width = 200, height = 100)

    bc = VerticalBarChart()
    bc.x = 20
    bc.data = [(int(info['executed'])*100/int(info['total_project']),),(100,)]
    # bc.labels = [str(x)+'%' for x in pc.data]

    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 20
    bc.valueAxis.visibleGrid = 1
    bc.valueAxis.gridStrokeColor = HexColor('#CCCCCC')
    bc.barSpacing = 3

    for i, color in enumerate(colors): 
        bc.bars[i].fillColor =  color

    bc.bars.strokeWidth = 0.01
    bc.bars.strokeColor = HexColor('#FFFFFF')

    legend = Legend()
    legend.fontName = 'Helvetica'
    legend.alignment = 'right'
    legend.columnMaximum = 1
    legend.y = -10
    legend.colorNamePairs = [(x,y) for x,y in zip(colors,['Presupuesto Ejecutado', 'Presupuesto Total'])]

    d2.add(legend)
    d2.add(bc)

    # y-cordinate doesn't quite align so we need some extra padding
    d2.drawOn(c, x+250, y - 20) 

    x = 88
    y -= 15

    for text in [note, signature]:
        y = y - h - leading

        if y <= 70:
            c.showPage()
            y = 720
        w, h = draw_text(c, text, x, y, 500, 500)

    # finish page
    c.showPage()
    # construct and save file to .pdf
    c.save() 