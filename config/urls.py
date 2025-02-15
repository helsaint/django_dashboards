"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('emissions/', include('emissions.urls')),
    path('pl_api/', include('pl_api.urls')),
    path('pl_results_api/', include('pl_results_api.urls')),
    path('web_scrape_api/', include('web_scrape_api.urls')),
    path('sofifa_api/', include('sofifa_api.urls')),
    path('', include('blackDB.urls')),
]
