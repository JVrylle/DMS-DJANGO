from django import template
register = template.Library()

@register.filter
def get_tooth(teeth_list, tooth_number):
    for t in teeth_list:
        if str(t.get('tooth')) == str(tooth_number):
            return t
    return {}