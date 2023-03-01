from django.shortcuts import render
from django.shortcuts import render
from .models import PremierLeague
from .serializers import PLSerializer
from rest_framework import generics

def pl_api(request):
    return render(request, "pl_api.html", {})

class GetPlayers(generics.ListAPIView):
    queryset = PremierLeague.objects.all()
    serializer_class = PLSerializer

# Create your views here.
