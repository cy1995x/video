# Generated by Django 2.2.5 on 2021-02-24 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_shortvideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortvideo',
            name='title',
            field=models.CharField(max_length=256),
        ),
    ]