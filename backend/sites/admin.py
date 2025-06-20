from django.contrib import admin

# Register your models here.
from .models import Site

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'topic')
    search_fields = ('title', 'topic')
