from django.db import models

class Prompt(models.Model):
    class Type(models.TextChoices):
        ARTICLE = "article", "Article"
        SOCIAL = "social", "Social"
        EMAIL = "email", "Email"

    site = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.ARTICLE)
    prompt_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("site", "name", "type")

    def __str__(self):
        return f"{self.site} - {self.name} ({self.type})"
