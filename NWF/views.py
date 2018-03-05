from django.views.generic import TemplateView, ListView
from game.models import Game

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(ListView):
    template_name = 'index.html'
    context_object_name = 'games'
    model = Game
