# In your app's templatetags directory
from django import template
from django.utils.numberformat import format as number_format

register = template.Library()

@register.filter
def currency_format(value):
    return number_format(value, decimal_pos=2, use_l10n=True)
