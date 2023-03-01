from django.urls import path
from . import views
from .views import GetPlayers

urlpatterns = [
    path('', views.pl_api, name='pl_api'),
    path('api_players', GetPlayers.as_view(), name='api_players')
]