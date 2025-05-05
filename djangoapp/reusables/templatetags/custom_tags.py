from django import template

register = template.Library()

@register.filter
def index_filter(sequence, position):
    return sequence[position]