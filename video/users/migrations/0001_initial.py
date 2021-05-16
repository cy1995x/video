# Generated by Django 2.2.5 on 2021-02-20 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('gender', models.IntegerField(choices=[(1, '男'), (2, '女'), (0, '隐藏')], default=0)),
                ('email', models.EmailField(default='', max_length=254)),
                ('phone', models.CharField(max_length=11)),
                ('avatar', models.ImageField(default='avatars/default.jpg', upload_to='avatars/')),
                ('sign', models.CharField(default='', max_length=64)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='U2U',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateField(auto_now_add=True, null=True)),
                ('fans', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fans', to='users.Users')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='users.Users')),
            ],
            options={
                'db_table': 'u2u',
            },
        ),
    ]