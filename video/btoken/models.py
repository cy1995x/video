from django.db import models

# Create your models here.
from users.models import Users


class Token(models.Model):
    user = models.OneToOneField(to=Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
