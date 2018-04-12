from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.urls import reverse_lazy, reverse
from game.forms import game_create_form
from game.models import Game,  InGame
from submissions.models import magic_card
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic.base import RedirectView
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib.auth import get_user, get_user_model

# Create your views here.

User=get_user_model()

class CreateGameView(FormView):
    model = Game
    template_name = 'game/game_create.html'
    form_class = game_create_form
    success_url = reverse_lazy('game:waiting')


    def form_valid(self, form):
        form.save()
        game = form.instance
        game.card_name = game.get_card_name()
        game.save()
        InGame.objects.create(player=self.request.user, game=game, score=0)

        return super().form_valid(form)

class Waiting(TemplateView):
    template_name = "game/waiting.html"

class GameDetail(DetailView):
    context_object_name = 'game_details'
    model = Game
    template_name = 'game/game_detail.html'
    success_url = reverse_lazy('game:waiting')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class JoinGame(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('game:game_details', kwargs={'pk': self.kwargs.get('pk')})

    def get(self,request,*args,**kwargs):
        game = get_object_or_404(Game, pk=self.kwargs.get('pk'))
        game.start = True
        game.in_progress= True
        try:
            InGame.objects.create(player=self.request.user, game=game)
        except IntegrityError:
            messages.warning(self.request, 'You have already joined this game')
        else:
            messages.success(self.request, 'You have successfully joined this game')

        return super().get(request,*args, **kwargs)


class StartGame(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=self.kwargs.get('pk'))
        game.in_progress = True
        game.start = True
        for player in game.players.all():
            card = magic_card.objects.create(player=player, game=game, card_name=game.card_name, round_submitted=game.round)
            card.save()
        game.save()
        return super().get(request,*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('submissions:card_submission', kwargs={'pk':self.kwargs.get('pk')})


class SelectCard(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        game = Game.objects.get(pk=self.kwargs.get('pk'))
        player = User.objects.get(username=self.kwargs.get('player'))
        card = magic_card.objects.get(game=game, player=player, card_name=game.card_name)
        update = InGame.objects.get(game=game, player=player)
        game.round += 1
        game.card_name = game.get_card_name()
        if game.judging == game.players.count()-1:
            game.judging = 0
        else:
            game.judging += 1
        game.save()
        for player in game.players.all():
            new_cards = magic_card.objects.create(player=player, game=game, round_submitted=game.round, card_name=game.card_name)
            new_cards.save()
        update.score += 1
        update.save()
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('game:game_details', kwargs={'pk': self.kwargs.get('pk')})
