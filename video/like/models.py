from django.db import models

from movies.models import Movies
from users.models import Users


class Like(models.Model):
    is_up = models.BooleanField()
    movie = models.ForeignKey(to=Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    class Meta:
        db_table = 'like'
