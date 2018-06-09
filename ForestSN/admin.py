from django.contrib import admin
from .models import UserProfile, Post, ExternalSocialNetwork

admin.site.register(UserProfile)


class PostAdmin(admin.ModelAdmin):

    list_display = ['author', 'short_text', 'pub_date']

admin.site.register(ExternalSocialNetwork)
admin.site.register(Post, PostAdmin)
