# Generated by Django 2.2.5 on 2021-02-24 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('movies', '0002_movies_movie_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('poster', models.ImageField(default='poster/default.jpg', upload_to='poster/')),
                ('video_file', models.FileField(default='shortvideo/default.mp4', upload_to='shortvideo/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users')),
            ],
            options={
                'db_table': 'shortvideo',
            },
        ),
    ]