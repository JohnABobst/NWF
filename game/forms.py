from django.forms import ModelForm
from game.models import Game
from django import forms
import random
import string


class game_create_form(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('number_of_players', 'number_of_rounds')
