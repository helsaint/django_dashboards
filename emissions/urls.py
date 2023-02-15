from django.urls import path
from . import views

urlpatterns = [
    path('emissions', views.emissions, name='emissions'),
    path('', views.emissions, name='emissions'),
]