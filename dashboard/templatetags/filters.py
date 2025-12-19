# dashboard/templatetags/filters.py
from django import template

register = template.Library()

@register.filter
def absval(value):
    """Return the absolute value of a number."""
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return 0
