from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    wall_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wall_owners')
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    parent_post = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='children', null=True,
        blank=True, default=None
    )
    root_post = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='descendants', null=True,
        blank=True, default=None
    )
    text = models.TextField(max_length=1000, blank=True)
    # TODO attachments
