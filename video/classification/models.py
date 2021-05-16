from django.db import models

from movies.models import Movies


class Classification(models.Model):
    classification = models.CharField(max_length=32)
    movie = models.ManyToManyField(to=Movies)


