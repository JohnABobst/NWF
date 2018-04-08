from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from submissions.views import CardSubmissionView, WaitingSubmissions
from . import views
app_name = 'submissions'

urlpatterns = [
    path('waiting_submissions', views.WaitingSubmissions.as_view(),
    name='waiting_submissions'),
    path('card_submission/<slug:pk>/<str:username>', views.CardSubmissionView.as_view(),
    name='card_submission'),
    path('card_details/<slug:pk>/<str:username>/<str:round_submitted>', views.CardDetailView.as_view(),
    name='card_details'),


]
