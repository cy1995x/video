# Generated by Django 2.2.5 on 2021-02-20 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('rank', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32)),
                ('actor', models.CharField(default='', max_length=128)),
                ('release_time', models.DateField(auto_now_add=True)),
                ('score', models.FloatField(default=0.0)),
                ('poster', models.ImageField(default='posters/default.jpeg', upload_to='posters/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users')),
            ],
            options={
                'db_table': 'movies',
            },
        ),
        migrations.CreateModel(
            name='MoviesDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_area', models.CharField(default='未知', max_length=32)),
                ('film_length', models.CharField(default='未知', max_length=32)),
                ('desc', models.TextField(null=True)),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='movies.Movies')),
            ],
            options={
                'db_table': 'movies_detail',
            },
        ),
        migrations.CreateModel(
            name='MoviesClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.CharField(max_length=16)),
                ('movie', models.ManyToManyField(to='movies.Movies')),
            ],
            options={
                'db_table': 'movies_classification',
            },
        ),
    ]