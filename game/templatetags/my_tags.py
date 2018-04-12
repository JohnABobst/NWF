from django import template
from game.models import Game, InGame
from django.contrib.auth import get_user_model
from submissions.models import magic_card
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


@register.simple_tag()
def submission_url(instance, duder):
    if instance.in_progress == True:
        thisplayer = User.objects.get(username=duder)
        card = magic_card.objects.get(game=instance, player=thisplayer, round_submitted=instance.round)
        return card.pk
