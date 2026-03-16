"""Custom template filters for documentation app."""

from datetime import datetime
from django import template

register = template.Library()


@register.filter(name='null_display')
def null_display(value, default='—'):
    """
    Return default string when value is None, empty string, or (optionally) empty list/dict.
    Usage: {{ value|null_display:"—" }} or {{ value|null_display }}
    """
    if default is None:
        default = '—'
    if value is None:
        return default
    if isinstance(value, str) and value.strip() == '':
        return default
    return value


@register.filter(name='format_datetime')
def format_datetime(value):
    """
    Format ISO timestamp or date string to human-readable (e.g. Jan 20, 2026).
    Returns original value if not parseable.
    """
    if value is None:
        return ''
    if hasattr(value, 'strftime'):
        return value.strftime('%b %d, %Y')
    s = str(value).strip()
    if not s:
        return ''
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            dt = datetime.strptime(s[:19], fmt)
            return dt.strftime('%b %d, %Y')
        except (ValueError, TypeError):
            continue
    return value


@register.filter(name='is_dict')
def is_dict(value):
    """Return True if value is a dict. Usage: {% if value|is_dict %}"""
    return isinstance(value, dict)


@register.filter(name='is_list')
def is_list(value):
    """Return True if value is a list. Usage: {% if value|is_list %}"""
    return isinstance(value, list)


@register.filter(name='replace')
def replace(value, arg):
    """
    Replace occurrences of a substring in a string.
    
    Supports two syntaxes:
    1. {{ value|replace:"old,new" }} - comma-separated
    2. {{ value|replace:"old":"new" }} - Django-style (requires custom tag)
    
    For Django-style, use: {{ value|replace_:"_":" " }}
    """
    if not value:
        return value
    
    if not arg:
        return value
    
    # Handle comma-separated format: "old,new"
    if ',' in arg:
        old, new = arg.split(',', 1)
        return str(value).replace(old, new)
    
    # If no comma, return as-is (might be used with replace_ tag)
    return str(value)


@register.simple_tag(name='replace_')
def replace_tag(value, old_str, new_str):
    """
    Template tag version of replace that accepts two separate arguments.
    
    Usage: {% replace_ value "_" " " %}
    """
    if not value:
        return value
    return str(value).replace(old_str, new_str)
