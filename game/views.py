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
from django.conf import settings

# Create your views here.

User=get_user_model()


def get_card(game, player):
    try:
        this_card = magic_card.objects.get(player=player, game=game,round_submitted=game.round)
        return(this_card)
    except:
        this_card = magic_card.objects.create(player=player, game=game, card_name=game.card_name, round_submitted=game.round)
        this_card.save()
        return(this_card)

class CreateGameView(FormView):
    model = Game
    template_name = 'game/game_create.html'
    form_class = game_create_form
    success_url = reverse_lazy('game:waiting')
    def form_valid(self, form):
        form.save()
        game = form.instance
        game.card_name = game.get_card_name()
        game.name = game.game_name()
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
            if magic_card.objects.filter(player=player, game=game, card_name=game.card_name, round_submitted=game.round).exists() == False:
                card = magic_card.objects.create(player=player, game=game, card_name=game.card_name, round_submitted=game.round)
                card.save()

        for player in game.players.all():
            card = get_card(game, player)
            list = []
            list.append(str(player.email))
            if player != game.judge():

                subject = 'Your game has started!'
                message = ('Enough players have signed up to begin playing.  Follow the link to submit a card.' + "\n <href= 'http://www.nerdsconamigos.com/submissions/card_submission/" + str(card.pk)
        +"'>")
                send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                list,
            )
            else:

                subject = "Your game has started!"
                message = "You are the judge this round, we will let you know once all cards have been submitted."
                send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                list,)

        game.save()
        return super().get(request,*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        game = get_object_or_404(Game, pk=self.kwargs.get('pk'))
        card = get_card(game, self.request.user)
        if self.request.user == game.judge():
            return reverse('game:game_details', kwargs={'pk':game.pk})
        else:
            return reverse('submissions:card_submission', kwargs={'pk':card.pk})

class SubmitCard(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        game = get_object_or_404(Game, pk=self.kwargs.get('pk'))
        card = get_card(game, self.request.user)
        card.submitted = True
        cards_submitted_this_round = magic_card.objects.filter(game=game, round_submitted=game.round, submitted = True)
        if cards_submitted_this_round.count() == game.number_of_players -1:
            subject = 'All players have submitted their cards this round'
            message = ('Follow the link to view the cards'+ "\n <href= 'http://www.nerdsconamigos.com/game/game_details/" + str(game.pk)+"'>")
            game.notify_players(subject,message)
        return reverse('submissions:card_submission', kwargs={'pk':card.pk})



class SelectCard(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        game = Game.objects.get(pk=self.kwargs.get('pk'))
        player = User.objects.get(username=self.kwargs.get('player'))
        card = get_card(game, player)
        update = InGame.objects.get(game=game, player=player)
        subject = 'A card has been chosen'
        message = ('Follow the link to see which card won this round' + "\n <href= 'http://www.nerdsconamigos.com/submissions/card_detail/" + str(card.pk)+"'>")
        game.notify_players(subject, message)
        game.round += 1
        if game.round > game.number_of_rounds:
            game.completed = True
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
