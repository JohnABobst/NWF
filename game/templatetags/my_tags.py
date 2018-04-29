from django import template
from game.models import Game, InGame
from django.contrib.auth import get_user_model
from submissions.models import magic_card
register = template.Library()


User = get_user_model()

@register.simple_tag()
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
        try:
            thisplayer = User.objects.get(username=duder)
            card = magic_card.objects.get(game=instance, player=thisplayer, round_submitted=instance.round)

        except:
            pass

        else:
            return card.pk


@register.simple_tag()
def available_games(games, user):

    for game in games:
        available = False
        if game.in_progress == False and user in game.players.all():
            available = True
        return available

@register.simple_tag()
def winner(instance):
    scores = {}
    for player in instance.players.all():
        score = InGame.objects.get(game=instance, player=player)
        scores[player] = score.score
    return max(scores, key=scores.get)

@register.simple_tag()
def has_submitted(instance, player):
    submitted = False
    if instance.in_progress == True:
        try:
            card = magic_card.objects.get(game=instance, player=player, card_name=instance.card_name)
            if card.submitted == True:
                submitted = True
        except:
            submitted = False

    return submitted

# Code to create a list of rounds i.e '123' so that they can be looped through in template.
@register.simple_tag()
def rounds_as_list(instance):
    list = []
    for i in range(1, (instance.round) ,1):
        list.append(i)
    return list
