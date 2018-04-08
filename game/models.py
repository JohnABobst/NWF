from django.db import models
from django.utils.text import slugify
# Create your models here.
import misaka
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, resolve, reverse
from django.contrib.auth import get_user_model
from django import template
register = template.Library()
import sys
import random
import string
import os

User = get_user_model()

class Game(models.Model):
    start = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    judging = models.IntegerField(default=0)
    round = models.IntegerField(default=1)
    number_of_players = models.IntegerField()
    number_of_rounds = models.IntegerField()
    players = models.ManyToManyField(User, through='InGame')

    def get_card_name():





    def is_juding(self):
        judges = list(self.players)
        return judges[self.judging]



class InGame(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    class Meta:
        unique_together = ('game', 'player')
