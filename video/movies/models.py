from django.db import models

# Create your models here.
from users.models import Users


class Movies(models.Model):
    rank = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=32)
    actor = models.CharField(max_length=128, default='')
    release_time = models.DateField(auto_now_add=True)
    score = models.FloatField(default=0.0)
    poster = models.ImageField(upload_to='posters/', default='posters/default.jpeg')
    movie_file = models.FileField(upload_to='myvideo/', default='myvideo/default.webm')
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    def __str__(self):
        return f'top100:{self.rank}'

    class Meta:
        db_table = 'movies'


# 电影细节
class MoviesDetail(models.Model):
    release_area = models.CharField(max_length=32, default='未知')
    film_length = models.CharField(max_length=32, default='未知')
    desc = models.TextField(null=True)
    movie = models.OneToOneField(to=Movies, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movies_detail'


# 电影分类
class MoviesClassification(models.Model):
    classification = models.CharField(max_length=16)
    movie = models.ManyToManyField(to=Movies)

    class Meta:
        db_table = 'movies_classification'


# 热门短视频
class ShortVideo(models.Model):
    title = models.CharField(max_length=256)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    poster = models.ImageField(upload_to='poster/', default='poster/default.jpg')
    video_file = models.FileField(upload_to='shortvideo/', default='shortvideo/default.mp4')

    class Meta:
        db_table = 'shortvideo'
