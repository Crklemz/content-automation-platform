from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Site
from .serializers import SiteSerializer
import json
from django.http import JsonResponse
from pathlib import Path

class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    lookup_field = 'slug'

def site_config_list(request):
    path = Path(__file__).resolve().parent.parent.parent / 'data' / 'site_config.json'
    with open(path) as f:
        config = json.load(f)
    return JsonResponse(config, safe=False)