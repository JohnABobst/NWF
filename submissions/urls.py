from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from submissions.views import CardSubmissionView
from . import views
# from game.views import GameDetailView

app_name = 'submissions'

urlpatterns = [
    path('waiting_submissions', views.WaitingSubmissions.as_view(),
    name='waiting_submissions'),
    path('card_submission/<slug:pk>', views.CardSubmissionView.as_view(),
    name='card_submission'),
    path('card_detail/<slug:pk>/', views.CardDetailView.as_view(),
    name='card_details'),
    path('', include('game.urls', namespace='game')),


]
