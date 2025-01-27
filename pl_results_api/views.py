from django.shortcuts import render
from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
from rest_framework import generics

@api_view(['GET'])
def pl_results_api(request):
    try:
        response = requests.get("https://fixturedownload.com/feed/json/epl-2024")
        return JsonResponse(response.json(), safe=False)
    except:
        return render(request, "pl_results_api.html",{})

# Create your views here.
