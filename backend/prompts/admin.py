from django.contrib import admin
from .models import Prompt

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("name", "site", "type", "created_at", "updated_at")
    list_filter = ("site", "type")
    search_fields = ("name", "prompt_text")
