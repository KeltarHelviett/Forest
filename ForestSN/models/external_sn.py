from django.db import models
from django.contrib.auth.models import User

class ExternalSocialNetwork(models.Model):
    name = models.CharField(max_length=256, unique=True)
    url = models.CharField(max_length=256, unique=True)

class ExternalSocialNetworkSession(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=256, unique=True)
    ext_user_id = models.BigIntegerField(unique=True, null=True)
    ext_social_network = models.ForeignKey(ExternalSocialNetwork, on_delete=models.CASCADE)
