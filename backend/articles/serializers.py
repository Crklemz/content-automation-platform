from rest_framework import serializers
from .models import Article
from sites.models import Site

class ArticleSerializer(serializers.ModelSerializer):
    site = serializers.SlugRelatedField(slug_field='slug', queryset=Site.objects.all())
    
    class Meta:
        model = Article
        fields = ['id', 'site', 'title', 'slug', 'body', 'sources', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_slug(self, value):
        # Ensure slug is unique across all articles
        if Article.objects.filter(slug=value).exists():
            raise serializers.ValidationError("An article with this slug already exists.")
        return value
    
    def validate_status(self, value):
        # Only allow valid status transitions
        valid_statuses = ['pending', 'approved', 'rejected']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value
