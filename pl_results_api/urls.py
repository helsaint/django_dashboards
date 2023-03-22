from django.urls import path
from .views import pl_results_api

urlpatterns = [
    path('pl_results_api', pl_results_api, name='pl_results_api'),
]