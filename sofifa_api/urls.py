from django.urls import path
from . import views
from .views import GeneralAllView

urlpatterns = [
    path('', views.sofifa_general_api_default, name='sofifa_general_api_default'),
    path('sofifa_general_stats_api', views.generalPlayerStats, name='sofifa_general_stats_api'),
    path('sofifa_general_api', GeneralAllView.as_view(), name='sofifa_general_api'),
    path('sofifa_bubble_plot_earnings_api', views.bubblePlotEarning, name='sofifa_bubble_plot_earnings_api'),
    path('sofifa_choropleth_api', views.choroplethData, name='sofifa_choropleth_api')
]