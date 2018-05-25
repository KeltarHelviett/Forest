from django.db import models
from django.contrib.auth.models import User
from .user_image import UserImage

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    profile_img = models.ForeignKey(UserImage, on_delete=models.SET_NULL, null=True)

    def profile_img_url(self):
        if self.profile_img is not None:
            return self.profile_img.img.url
        return 'https://i.pinimg.com/564x/5b/70/d1/5b70d179c4e8a58fa4f2ac6ae0ea5ba1.jpg'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
