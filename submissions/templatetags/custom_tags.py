from django import template

register = template.Library()
# code to determine which player is judging
@register.simple_tag()
def is_judging(list, index):

    return list[index]

# Code to create a list of rounds i.e '123' so that they can be looped through in template.
@register.simple_tag()
def rounds_as_string(instance):
    list = ''
    for i in range (1, (instance.round-1) ,1):
        list.append(str(i))
    return list
