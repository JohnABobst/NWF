from django.forms import ModelForm
from game.models import Game
from submissions.models import magic_card
from django import forms
import random
import string

class CardSubmission(forms.ModelForm):

    class Meta:
        model = magic_card
        fields = [ 'converted_mana_cost', 'card_color','card_type','card_text', 'flavor_text']
