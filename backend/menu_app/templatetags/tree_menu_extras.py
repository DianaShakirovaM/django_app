from django import template

register = template.Library()


@register.filter
def has_children(item):
    return len(item.children) > 0
