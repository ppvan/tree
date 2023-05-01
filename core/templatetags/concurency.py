# myapp/templatetags/my_filters.py

from django import template
from django.utils import formats
from django.contrib.humanize.templatetags import humanize

register = template.Library()


@register.filter
def vnd_format(value):
    """Converts a decimal number to Vietnamese currency format."""
    return humanize.intcomma(value, False).replace(",", ".") + " ₫"
