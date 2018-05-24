from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    parent_post = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='parent_post_set',
        null=True
    )
    root_post = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='root_post_set',
        null=True
    )
    text = models.TextField(max_length=1000, blank=True)
    # TODO attachments
