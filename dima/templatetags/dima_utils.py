from django import template

register = template.Library()


# @register.filter
# def replace(string, old_string, new_string):
    # return string.replace(old_string, new_string)


@register.simple_tag(name='replace')
def replace(string, old_string, new_string):
    return string.replace(old_string, new_string).strip()

@register.filter(name='untagged')
def untagged(string):
    start = string.index('>')
    string = string[start+1:]
    end = string.index('<')
    return string[:end]