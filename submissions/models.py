from django.db import models
from game.models import Game
from django.contrib.auth import get_user_model


User=get_user_model()
# Create your models here.
class magic_card(models.Model):


    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    round_submitted = models.IntegerField()
    chosen = models.BooleanField(default=False)
    card_name = models.CharField(max_length=1000)
    submitted = models.BooleanField(default=False)
    BLUE = "Blue"
    RED = "Red"
    WHITE = "White"
    BLACK = "Black"
    GREEN = "Green"
    COLORLESS = "Colorless"
    mana_colors = (
        (BLUE, "Blue"),
        (RED, "Red"),
        (WHITE, "White"),
        (BLACK, "Black"),
        (GREEN, "Green"),
        (COLORLESS, "Colorless"),
        )

    ENCHANTMENT = "Enchantment"
    ARTIFACT = "Atifact"
    CREATURE = "Creature"
    LAND = "Land"
    PLANESWALKER = "Planeswalker"
    SORCERY = "Sorcery"
    INSTANT = "Instant"

    card_types = (
        (ENCHANTMENT, "Enchantment"),
        (ARTIFACT, "Artifact"),
        (CREATURE, "Creature"),
        (LAND, "Land"),
        (PLANESWALKER, "Planeswalker"),
        (SORCERY, "Sorcery"),
        (INSTANT, "Instant")
    )


    card_color = models.CharField(
        max_length = 15,
        choices = mana_colors
    )

    card_type = models.CharField(
        max_length = 256
    )



    converted_mana_cost = models.CharField(max_length=240, default="i.e 2GG for 2 colorless and 2 Green")

    card_text = models.TextField(default='card text')

    flavor_text = models.TextField(default = "flavor text")


    def get_absolute_url(self):
        return reverse('submissions', kwargs={'username': self.user.username, 'pk':self.pk})


    def __str__(self):
        return str(self.pk)

    def save(self, *args,**kwargs):
        return super().save(*args,**kwargs)
