from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        site_slug = self.request.query_params.get('site')
        if site_slug:
            return Article.objects.filter(site__slug=site_slug, status='approved')
        return Article.objects.filter(status='approved')
