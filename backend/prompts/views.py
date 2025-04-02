from rest_framework.viewsets import ModelViewSet
from .models import Prompt
from .serializers import PromptSerializer

class PromptViewSet(ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
