from django import template

register = template.Library()

@register.filter
def percent(value):
    """Format a float number as a percentage with 2 decimals"""
    assert type(value) == float or value == None, "Value given isn't a float"
    if value:
        return f'{value*100.0:.2f}%'
    else:
        return value

@register.filter
def date_to_html(value):
    """Format a date from dd/mm/yyyy to yyyy-mm-dd"""
    assert type(value) == str or value == None, "Value given isn't a float"
    if value:
        value = value.split('/')
        if len(value[1]) == 1:
            value[1] = '0'+value[1]
        if len(value[0]) == 1:
            value[0] = '0'+value[0]
        value[2] = value[2].split()[0]
        return f'{value[2]}-{value[1]}-{value[0]}'
    else:
        return value