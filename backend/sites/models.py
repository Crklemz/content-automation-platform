from django.db import models

# Create your models here.
from django.db import models

class Site(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    logo = models.CharField(max_length=255)

    # Branding colors
    primary_color = models.CharField(max_length=7)
    secondary_color = models.CharField(max_length=7)
    tertiary_color = models.CharField(max_length=7, blank=True)
    quaternary_color = models.CharField(max_length=7, blank=True)

    def __str__(self):
        return self.title
