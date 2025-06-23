from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'site', 'status', 'created_at', 'status_color']
    list_filter = ['status', 'site', 'created_at']
    search_fields = ['title', 'body', 'site__name']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    # Custom admin actions
    actions = ['approve_articles', 'reject_articles']
    
    def status_color(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': '#ffa500',    # Orange
            'approved': '#28a745',   # Green
            'rejected': '#dc3545',   # Red
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_color.short_description = 'Status'
    
    def approve_articles(self, request, queryset):
        """Bulk action to approve selected articles"""
        updated = queryset.update(status='approved')
        self.message_user(
            request,
            f'Successfully approved {updated} article(s).'
        )
    approve_articles.short_description = "Approve selected articles"
    
    def reject_articles(self, request, queryset):
        """Bulk action to reject selected articles"""
        updated = queryset.update(status='rejected')
        self.message_user(
            request,
            f'Successfully rejected {updated} article(s).'
        )
    reject_articles.short_description = "Reject selected articles"
    
    # Customize the form
    fieldsets = (
        ('Content', {
            'fields': ('site', 'title', 'slug', 'body')
        }),
        ('Metadata', {
            'fields': ('sources', 'status', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Auto-generate slug from title
    prepopulated_fields = {'slug': ('title',)}
