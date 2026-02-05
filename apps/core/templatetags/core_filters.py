"""Core template filters for shared use across apps."""

from datetime import datetime
from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter(name='timesince_safe')
def timesince_safe(value):
    """
    Like timesince but accepts ISO date strings from JSON/S3 storage.
    
    Usage: {{ workflow.updated_at|timesince_safe }}
    Returns 'ago' suffix text (e.g. "2 hours ago") or empty string if invalid.
    """
    if value is None or value == '':
        return ''
    if hasattr(value, 'year'):
        return timesince(value)
    if isinstance(value, str):
        try:
            s = value.replace('Z', '+00:00')
            dt = datetime.fromisoformat(s)
            return timesince(dt)
        except (ValueError, AttributeError, TypeError):
            try:
                dt = datetime.fromisoformat(value.split('.')[0].replace('Z', '+00:00'))
                return timesince(dt)
            except (ValueError, AttributeError, TypeError, IndexError):
                return ''
    return ''
