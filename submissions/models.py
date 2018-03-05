from django.db import models
from game.models import Game
from django.contrib.auth import get_user_model
import random
import string

User=get_user_model()
# Create your models here.
class magic_card(models.Model):
    
    def gen_card_name():
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(5))

    card_name = models.CharField(max_length=256, default='card name')

    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    game= models.ForeignKey(Game, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)

    round_submitted = models.IntegerField(default=1)

    BLUE = "U"
    RED = "R"
    WHITE = "W"
    BLACK = "B"
    GREEN = "G"

    mana_colors = (
        (BLUE, "Blue"),
        (RED, "Red"),
        (WHITE, "White"),
        (BLACK, "Black"),
        (GREEN, "Green"),
        )

    ENCHANTMENT = "EN"
    ARTIFACT = "AR"
    CREATURE = "CR"
    LAND = "LA"
    PLANESWALKER = "PL"

    card_types = (
        (ENCHANTMENT, "Enchantment"),
        (ARTIFACT, "Artifact"),
        (CREATURE, "Creature"),
        (LAND, "Land"),
        (PLANESWALKER, "Planeswalker"),
    )


    card_color = models.CharField(
        max_length = 5,
        choices = mana_colors
    )

    card_type = models.CharField(
        max_length = 5,
        choices = card_types
    )


    converted_mana_cost = models.CharField(max_length=240, default="0")

    card_text = models.CharField(max_length = 240, default='card text')

    flavor_text = models.CharField(max_length = 240, default = "flavor text")


    def get_absolute_url(self):
        return reverse('submissions', kwargs={'username': self.user.username, 'pk':self.pk})


    def __str__(self):
        return str(self.pk)

    def save(self, *args,**kwargs):
        return super().save(*args,**kwargs)
