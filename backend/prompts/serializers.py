from rest_framework import serializers
from .models import Prompt

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = [
            "id",
            "site",
            "name",
            "type",
            "prompt_text",
            "created_at",
            "updated_at",
        ]
