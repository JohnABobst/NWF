from django.shortcuts import render, get_object_or_404
from submissions.forms import CardSubmission
from submissions.models import magic_card
from game.models import Game
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
# Create your views here.
user = get_user_model()

class WaitingSubmissions(TemplateView):
    template_name = 'submissions/waiting_submissions.html'

class CardSubmissionView(FormView):
    model = magic_card
    template_name = 'submissions/card_submission.html'
    success_url = reverse_lazy('submissions:waiting_submissions')
    form_class = CardSubmission



    def form_valid(self, form):

        submission = form.save(commit=False)
        form.instance.player = self.request.user
        form.instance.game = Game.objects.get(players=self.request.user, pk=self.kwargs.get('pk'))
        submission.card_name = form.card_name

        submission.save()

        return super().form_valid(form)
