# Generated by Django 4.2.3 on 2023-08-17 11:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='post_images')),
                ('caption', models.TextField()),
                ('created_at', models.DateField(default=datetime.datetime.now)),
                ('add_favourite', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id_profile', models.AutoField(primary_key=True, serialize=False)),
                ('bio', models.TextField(blank=True)),
                ('profileimg', models.ImageField(default='blank-profile-picture-gf4cd40bc5_1280.png', upload_to='profile_images')),
                ('location', models.CharField(blank=True, max_length=100)),
                ('no_of_winks', models.ManyToManyField(related_name='profile_winked', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]