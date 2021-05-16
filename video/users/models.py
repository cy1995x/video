from django.db import models


# Create your models here.

class Users(models.Model):
    gender_choices = (
        (1, '男'),
        (2, '女'),
        (0, '隐藏')
    )
    nickname = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    gender = models.IntegerField(choices=gender_choices, default=0)
    email = models.EmailField(default='')
    phone = models.CharField(max_length=11, null=False)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    sign = models.CharField(max_length=64, default='')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"用户：{self.nickname}"

    class Meta:
        db_table = 'users'


class U2U(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name='user')
    fans = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name='fans')
    created_time = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'u2u'
