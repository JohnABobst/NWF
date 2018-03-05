from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.urls import reverse_lazy, reverse
from game.forms import game_create_form
from game.models import Game,  InGame
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic.base import RedirectView
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib.auth import get_user
# Create your views here.



class CreateGameView(FormView):
    model = Game
    template_name = 'game/game_create.html'
    form_class = game_create_form
    success_url = reverse_lazy('game:waiting')


    def form_valid(self, form):
        form.save()
        game = form.instance
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
        game.save()
        return super().get(request,*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('submissions:card_submission', kwargs={'pk':self.kwargs.get('pk'), 'username': self.request.user })
