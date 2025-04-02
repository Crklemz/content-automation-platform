"""
Main URL configuration for the Content Automation Platform backend.
Includes API routes and Django admin.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from articles.views import ArticleViewSet
from prompts.views import PromptViewSet

router = DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"prompts", PromptViewSet, basename="prompt")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
