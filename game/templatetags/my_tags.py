from django import template
from game.models import Game, InGame
from django.contrib.auth import get_user_model
register = template.Library()

User = get_user_model()
@register.simple_tag
def is_judging(list, index):

    return list[index]


@register.simple_tag()
def player_score(instance, duder):

    thisplayer= User.objects.get(username=duder)
    scores = InGame.objects.get(game=instance, player=thisplayer)
    return scores.score
