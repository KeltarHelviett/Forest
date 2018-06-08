from django.contrib.auth.models import User
from django.db import models

from secrets import token_urlsafe

from ..models import ExternalSocialNetwork

class AuthorizationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=256)
    # expiration_datetime

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = token_urlsafe(32)
        super(AuthorizationCode, self).save(*args, **kwargs)

class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=256)
    app_name = models.CharField(max_length=200) # should be client_id or smth
    # expiration_date

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = token_urlsafe(32)
        super(AccessToken, self).save(*args, **kwargs)
