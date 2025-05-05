from django import template

register = template.Library()

@register.filter
def index_filter(sequence, position):
    return sequence[position]

@register.filter
def add_class(field, css_class):
    if hasattr(field, 'errors') and field.errors:
        existing_classes = field.field.widget.attrs.get('class', '')
        css_class = existing_classes + ' ' + css_class + ' is-invalid'
    else:
        existing_classes = field.field.widget.attrs.get('class', '')
        css_class = existing_classes + ' ' + css_class

    return field.as_widget(attrs={"class": css_class})