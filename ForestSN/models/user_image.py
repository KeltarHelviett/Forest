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

models.signals.post_save.connect(rename_img, sender=UserImage)
