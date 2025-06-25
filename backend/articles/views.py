from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from django.http import HttpRequest
from typing import TYPE_CHECKING, cast
from services.content_automation import ContentAutomation
from sites.models import Site

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
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def generate_content(self, request):
        """Generate AI content for a site"""
        try:
            site_slug = request.data.get('site_slug')
            topic = request.data.get('topic')
            count = request.data.get('count', 1)
            
            if not site_slug:
                return Response(
                    {'error': 'site_slug is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                site = Site.objects.get(slug=site_slug)
            except Site.DoesNotExist:
                return Response(
                    {'error': f'Site with slug "{site_slug}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            automation = ContentAutomation()
            
            if topic:
                # Generate content for specific topic
                article = automation.generate_content_from_topic(topic, site)
                if article:
                    return Response({
                        'message': f'Generated article: {article.title}',
                        'article_id': article.pk
                    })
                else:
                    return Response(
                        {'error': 'Failed to generate article'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                # Generate content based on trending topics
                articles = automation.generate_content_for_site(site, count)
                return Response({
                    'message': f'Generated {len(articles)} articles for {site.name}',
                    'article_ids': [article.pk for article in articles]
                })
                
        except Exception as e:
            return Response(
                {'error': f'Error generating content: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def trending_topics(self, request):
        """Get trending topics for content generation"""
        try:
            site_slug = request.query_params.get('site_slug')
            category = request.query_params.get('category', 'general')
            limit = int(request.query_params.get('limit', 10))
            
            print(f"Trending topics request - site_slug: {site_slug}, category: {category}, limit: {limit}")
            
            automation = ContentAutomation()
            
            if site_slug:
                try:
                    site = Site.objects.get(slug=site_slug)
                    print(f"Found site: {site.name} with description: {site.description}")
                    topics = automation.get_trending_topics_for_site(site, limit)
                    print(f"Got {len(topics)} topics for site {site.name}")
                except Site.DoesNotExist:
                    print(f"Site with slug '{site_slug}' not found")
                    return Response(
                        {'error': f'Site with slug "{site_slug}" not found'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                print("No site_slug provided, getting general topics")
                topics = automation.get_general_trending_topics(category, limit)
                print(f"Got {len(topics)} general topics")
            
            print(f"Returning {len(topics)} topics")
            return Response({
                'topics': topics,
                'count': len(topics)
            })
            
        except Exception as e:
            print(f"Error in trending_topics endpoint: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Error fetching trending topics: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def news_summary(self, request):
        """Get news summary for a specific topic with sources"""
        try:
            topic = request.query_params.get('topic')
            site_slug = request.query_params.get('site_slug')
            
            if not topic:
                return Response(
                    {'error': 'topic parameter is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            automation = ContentAutomation()
            
            if site_slug:
                try:
                    site = Site.objects.get(slug=site_slug)
                    sources = automation._get_relevant_sources(topic, site)
                except Site.DoesNotExist:
                    return Response(
                        {'error': f'Site with slug "{site_slug}" not found'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                # Get general sources if no site specified
                sources = automation.news_scraper.get_trending_topics('general', limit=5)
            
            # Create a summary of the topic based on sources
            summary = automation._create_topic_summary(topic, sources)
            
            return Response({
                'topic': topic,
                'summary': summary,
                'sources': sources,
                'count': len(sources)
            })
            
        except Exception as e:
            return Response(
                {'error': f'Error creating news summary: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def generate_daily_top3(self, request):
        """Generate a Daily Top 3 article combining multiple topics"""
        try:
            site_slug = request.data.get('site_slug')
            topics = request.data.get('topics', [])
            
            if not site_slug:
                return Response(
                    {'error': 'site_slug is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not topics or len(topics) < 3:
                return Response(
                    {'error': 'At least 3 topics are required for Daily Top 3'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                site = Site.objects.get(slug=site_slug)
            except Site.DoesNotExist:
                return Response(
                    {'error': f'Site with slug "{site_slug}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            automation = ContentAutomation()
            
            # Generate Daily Top 3 article using the provided topics
            article = automation.generate_daily_top3_from_topics(site, topics[:3])
            
            if article:
                return Response({
                    'message': f'Generated Daily Top 3 article: {article.title}',
                    'article_id': article.pk
                })
            else:
                return Response(
                    {'error': 'Failed to generate Daily Top 3 article'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            return Response(
                {'error': f'Error generating Daily Top 3: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
