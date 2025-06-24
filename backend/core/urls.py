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
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
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
import json

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'sites', SiteViewSet, basename='site')

@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_staff:
        login(request, user)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    logout(request)
    return JsonResponse({'success': True})

@require_http_methods(["GET"])
def api_check_auth(request):
    if request.user.is_authenticated and request.user.is_staff:
        return JsonResponse({'authenticated': True})
    else:
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
