from django import template

register = template.Library()

bad_words = ['террорист', 'хулиган', 'преступление', 'насилие']

@register.filter()
def censor(value):
    for  bw in bad_words:
        value = value.lower().replace(bw.lower(), '*')
    return value