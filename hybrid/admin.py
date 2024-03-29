from django.contrib import admin
from .models import Profile, Post


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id_profile', 'user', 'bio', 'location')


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post)
