from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=25)
    streaming_key = models.CharField(max_length=255, null=True, blank=True)
    playback_url = models.CharField(max_length=255, null=True, blank=True)
    rtmps_server = models.CharField(max_length=255, null=True, blank=True)

