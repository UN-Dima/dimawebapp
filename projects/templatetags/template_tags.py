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