# Generated by Django 2.2.5 on 2021-02-23 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='movie_file',
            field=models.FileField(default='myvideo/default.webm', upload_to='myvideo/'),
        ),
    ]
