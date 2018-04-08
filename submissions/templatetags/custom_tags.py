from django import template

register = template.Library()

@register.simple_tag()
def is_judging(list, index):

    return list[index]
