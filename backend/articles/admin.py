from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "site", "status", "created_at", "updated_at")
    list_filter = ("status", "site")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
