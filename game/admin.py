from django.contrib import admin
from game.models import Game, InGame

# Register your models here.


class InGameInline(admin.TabularInline):
    model = InGame
    extra =1

class GameAdmin(admin.ModelAdmin):
    inlines = (InGameInline,)

class UserInline(admin.ModelAdmin):
    inlines = (InGameInline)

admin.site.register(Game)

admin.site.register(InGame)
