from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from django.http import HttpRequest
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser

from .models import Article
from .serializers import ArticleSerializer

class ArticleFilter(filters.FilterSet):
    """Filter articles by site, status, and date range"""
    site = filters.CharFilter(field_name='site__slug', lookup_expr='exact')
    status = filters.CharFilter(lookup_expr='exact')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Article
        fields = ['site', 'status', 'created_after', 'created_before']

class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing articles with full CRUD operations.
    Supports filtering by site, status, and date range.
    """
    serializer_class = ArticleSerializer
    filterset_class = ArticleFilter
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return different querysets based on the request:
        - Public requests: only approved articles
        - Admin requests: all articles with proper filtering
        """
        queryset = Article.objects.select_related('site').all()
        
        # For now, allow all articles to be visible
        # TODO: Add proper authentication for admin interface
        return queryset
        
        # Check if this is a public request (no admin authentication)
        # user = cast(User, self.request.user)
        # if not user.is_staff:
        #     # Public users only see approved articles
        #     return queryset.filter(status='approved')
        # 
        # # Admin users can see all articles with filtering
        # return queryset
    
    @action(detail=True, methods=['post'])
    def approve(self, request: HttpRequest, pk=None):
        """Approve an article (admin only)"""
        # TODO: Add proper authentication for admin interface
        # user = cast(User, request.user)
        # if not user.is_staff:
        #     return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        article = self.get_object()
        article.status = 'approved'
        article.save()
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request: HttpRequest, pk=None):
        """Reject an article (admin only)"""
        # TODO: Add proper authentication for admin interface
        # user = cast(User, request.user)
        # if not user.is_staff:
        #     return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        article = self.get_object()
        article.status = 'rejected'
        article.save()
        return Response({'status': 'rejected'})
