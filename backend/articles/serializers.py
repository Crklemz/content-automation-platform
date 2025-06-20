from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    site = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
