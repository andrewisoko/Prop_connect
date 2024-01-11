from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime


User = get_user_model()
# Create your models here.


class Profile(models.Model):
    id_profile = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to='profile_images', default='blank-profile-picture-gf4cd40bc5_1280.png')
    location = models.CharField(max_length=100, blank=True)
    no_of_winks = models.ManyToManyField(User, related_name='profile_winked')
    # age later on

    def __str__(self):
        return self.user.username

    def total_winks(self):
        return self.no_of_winks.count()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateField(default=datetime.now)
    add_favourite = models.IntegerField(default=0)

    def __str__(self):
        return self.user
