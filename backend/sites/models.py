from django.db import models

class Site(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.CharField(max_length=255)
    
    primary_color = models.CharField(max_length=7)
    secondary_color = models.CharField(max_length=7)
    # Optional extras for future theming
    tertiary_color = models.CharField(max_length=7, blank=True, default="")
    quaternary_color = models.CharField(max_length=7, blank=True, default="")

    def __str__(self):
        return self.name
