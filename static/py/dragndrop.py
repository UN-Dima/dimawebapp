from browser import document, bind, html, window, ajax, console, window

Date = window.Date.new

# ----------------------------------------------------------------------
@bind('.dima-dragndrop_area', 'dragover')
def ondrag(evt):
    """"""
    evt.stopPropagation()
    evt.preventDefault()
    evt.dataTransfer.dropEffect = 'copy'

# ----------------------------------------------------------------------


@bind('.dima-dragndrop_area', 'dragleave')
def ondrag(evt):
    """"""
    evt.stopPropagation()
    evt.preventDefault()
    evt.target.style = {'background-color': '#e7e7e7'}


# ----------------------------------------------------------------------
@bind('.dima-dragndrop_area', 'dragenter')
def ondrag(evt):
    """"""
    evt.stopPropagation()
    evt.preventDefault()
    evt.target.style = {'background-color': '#e1e1e1'}


# ----------------------------------------------------------------------
@bind('.dima-dragndrop_area', 'drop')
def ondrop(evt):
    evt.stopPropagation()
    evt.preventDefault()

    files = evt.dataTransfer.files  # FileList object.

    # files is a FileList of File objects. List some properties.
    _ul = html.UL(Class='dima-dragndrop_output')
    for f in files:
        last_mod = Date(f.lastModified) if f.lastModified else "n/a"
        _ul <= html.LI(f'>>> Enviando: {f.name} - ({f.size} bytes)')

    document.select_one('.dima-dragndrop_area') <= _ul

    input_ = document.select_one(".dima-dragndrop_input")
    input_.files = files
    form = document.select_one(f'.dima-dragndrop_form')
    form_data = ajax.form_data(form)

    req = ajax.ajax()
    req.open('POST', form.attrs['action'])
    req.send(form_data)

    def handle_response(req):

        if req.status == 200:
            for line in req.json['msg']:
                _ul <= html.LI(line)
            if req.json['redirect']:
                window.location.href = req.json['redirect']
        else:
            _ul <= html.LI('Se produjo un error al enviar el formulario')

    req.bind('complete', handle_response)

@bind("#AutoUpdate_Projects", "click")
def auto_aupdate_project(evt):
    # Create a loading screen
    d1 = html.DIV(Class="PopOut", id = "PopOutDiv")
    d2 = html.DIV(Class="flex-div")
    b = html.BUTTON(id="Close_Popup", Class="Button_Transparent")
    d3 = html.DIV(style={"background":"white", "margin":"auto"}, Class='Info_PopUp')
    loader = html.DIV(Class = 'loader') 
    d3 <= loader
    d3 <= html.P('Descargando archivo')
    d2 <= b
    d2 <= d3
    d1 <= d2
    document <= d1

    form = document.select_one(f'.dima-dragndrop_form')
    req = ajax.ajax()
    req.open('POST', form.attrs['action'])
    req.send(ajax.form_data())
    _ul = html.UL(Class='dima-dragndrop_output')

    def handle_response(req):

        if req.status == 200:
            for line in req.json['msg']:
                _ul <= html.LI(line)
            if req.json['redirect']:
                window.location.href = req.json['redirect']
        else:
            _ul <= html.LI('Se produjo un error al enviar el formulario')

        del d1

    req.bind('complete', handle_response)

