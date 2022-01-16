from turtle import title
from django.db import models

class GenreInfo (models.Model):
    """
    Information and media for each genre Jordan can play
    """
    title = models.CharField(max_length=50,)
    summary = models.TextField()
    image_one = models.ImageField(upload_to='', null=True, blank=True)
    image_two = models.ImageField(upload_to='', null=True, blank=True)
    image_three = models.ImageField(upload_to='', null=True, blank=True)
