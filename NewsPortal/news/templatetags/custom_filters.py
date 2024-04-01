from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def censor(value):
    bad_words = ['террорист', 'хулиган', 'преступление', 'насилие', 'подростки']
    
    if not isinstance(value, str):
        return ValueError('Применяется только к переменным строкового типа')
    for word in  bad_words:
        value = value.replace(word,'*' * len(word))
        
    return mark_safe(value)