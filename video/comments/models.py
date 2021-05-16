from django.db import models

from movies.models import Movies
from users.models import Users


class Comments(models.Model):
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(to=Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(to='self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'评论内容：{self.content}'

    class Meta:
        db_table = 'comments'
