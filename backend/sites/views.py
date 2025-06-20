from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Site
from .serializers import SiteSerializer

class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    lookup_field = 'slug'
