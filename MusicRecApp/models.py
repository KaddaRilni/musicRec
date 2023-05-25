from django.db import models

# Create your models here.

class Music(models.Model):
    path = models.CharField(max_length=255)
    melspec = models.JSONField()