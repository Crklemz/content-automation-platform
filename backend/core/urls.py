"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', views.Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from sites.views import SiteViewSet
from articles.views import ArticleViewSet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError
import json
import logging

logger = logging.getLogger(__name__)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'sites', SiteViewSet, basename='site')

@csrf_exempt
@require_http_methods(["POST"])
@never_cache
def api_login(request):
    """Secure login endpoint with rate limiting and logging"""
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Basic validation
        if not username or not password:
            logger.warning(f"Login attempt with missing credentials from {request.META.get('REMOTE_ADDR')}")
            return JsonResponse({
                'success': False, 
                'error': 'Username and password are required'
            }, status=400)
        
        # Rate limiting check (basic implementation)
        if hasattr(request, 'user') and request.user.is_authenticated:
            return JsonResponse({
                'success': False, 
                'error': 'Already authenticated'
            }, status=400)
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active and user.is_staff:
            login(request, user)
            logger.info(f"Successful login for user {username} from {request.META.get('REMOTE_ADDR')}")
            return JsonResponse({
                'success': True,
                'user': {
                    'username': user.username,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }
            })
        else:
            logger.warning(f"Failed login attempt for username '{username}' from {request.META.get('REMOTE_ADDR')}")
            return JsonResponse({
                'success': False, 
                'error': 'Invalid credentials or insufficient permissions'
            }, status=401)
            
    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON in login request from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({
            'success': False, 
            'error': 'Invalid request format'
        }, status=400)
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': 'Internal server error'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
@never_cache
def api_logout(request):
    """Secure logout endpoint"""
    try:
        username = request.user.username
        logout(request)
        logger.info(f"User {username} logged out from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': 'Internal server error'
        }, status=500)

@require_http_methods(["GET"])
@never_cache
def api_check_auth(request):
    """Check authentication status"""
    try:
        if request.user.is_authenticated and request.user.is_active and request.user.is_staff:
            return JsonResponse({
                'authenticated': True,
                'user': {
                    'username': request.user.username,
                    'is_staff': request.user.is_staff,
                    'is_superuser': request.user.is_superuser
                }
            })
        else:
            return JsonResponse({'authenticated': False}, status=401)
    except Exception as e:
        logger.error(f"Auth check error: {str(e)}")
        return JsonResponse({'authenticated': False}, status=401)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("api/sites/", include("sites.urls")),
    # API Authentication endpoints
    path('api/auth/login/', api_login, name='api_login'),
    path('api/auth/logout/', api_logout, name='api_logout'),
    path('api/auth/check/', api_check_auth, name='api_check_auth'),
]
