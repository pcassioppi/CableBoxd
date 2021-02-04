from django.db import models
from django.conf import settings

# Create your models here.
class Show(models.Model):
    title = models.CharField(max_length=100)
    years = models.CharField(max_length=50)
    poster = models.URLField()
    rating = models.CharField(max_length=5)
    summary = models.TextField(blank=True)
    creators = models.CharField(max_length=100)
    stars = models.CharField(max_length=100)
    

class SeenList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show = models.ForeignKey('shows.Show', related_name='seenLists', on_delete=models.CASCADE)
