from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from game.views import CreateGameView, GameDetail, Waiting, JoinGame, StartGame
from . import views



app_name = 'game'


urlpatterns = [


        path('create_game/', views.CreateGameView.as_view(),
        name='create_game'),
        path('waiting/', views.Waiting.as_view(),
        name='waiting'),

        path('game_details/<slug:pk>/', views.GameDetail.as_view(),
        name='game_details'),
        path('join/<slug:pk>/', views.JoinGame.as_view(),
        name='join'),
        
        path('start/<slug:pk>', views.StartGame.as_view(),
        name='start')




        ]
