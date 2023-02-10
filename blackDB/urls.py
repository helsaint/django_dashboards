from django.urls import path
from . import views

urlpatterns = [
    path('', views.blackdb_return, name='blackdb_return'),
    path('bar_chart_data', views.blackdb_chart_data, name='blackdb_chart_data'),
    path('max_population', views.max_population, name='max_population'),
    path('max_co2', views.max_co2,name='max_co2'),
    path('max_co2_per_capita', views.max_co2_per_capita, name='max_co2_per_capita'),
    path('max_cumulative_co2', views.max_cumulative_co2, name='max_cumulative_co2'),
    path('emissions_per_capita', views.emissions_per_capita, name='emissions_per_capita'),
]