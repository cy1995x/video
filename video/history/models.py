from django.db import models
from users.models import Users
from movies.models import Movies


# Create your models here.
class History(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    movie = models.ForeignKey(to=Movies, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'history'
