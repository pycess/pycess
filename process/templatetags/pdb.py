from django.template import Library

register = Library()

@register.filter 
def pdb(element):
    import pdb; pdb.set_trace()
    return element
