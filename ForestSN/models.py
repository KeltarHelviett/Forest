from django.db import models
from django.contrib.auth.models import User
import random, string, os
from Forest.settings import MEDIA_ROOT

def user_img_path(instanse, filename):
    path = 'imgs/user_{}/'.format(instanse.user.id) + 'img_{}{}'

    return path.format(
        ''.join([random.choice(string.ascii_letters + string.digits) for i in range(150)]),
        instanse.extension()
    )

def rename_img(sender, instance, created, **kwargs):
    if created:
        new_name = 'imgs/user_{}/img_{}{}'.format(
            instance.user.id,
            instance.id,
            instance.extension()
        )
        new_path = '{}/{}'.format(MEDIA_ROOT, new_name)
        os.rename(instance.img.path, new_path)
        instance.img.name = new_name
        instance.save()

class UserImage(models.Model):
    # TODO album = models.FK(Album, null=True)
    img = models.ImageField(upload_to=user_img_path)
    caption = models.CharField(max_length=300, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # pub_date = models.DateTimeField('publication date')

    def extension(self):
        return os.path.splitext(self.img.name)[1]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    profile_img = models.ForeignKey(UserImage, on_delete=models.SET_NULL, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
models.signals.post_save.connect(rename_img, sender=UserImage)
