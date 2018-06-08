from django.contrib.auth.models import User
from django.db import models

class AuthorizationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=256)
    # expiration_datetime

class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=256)
    # expiration_date
