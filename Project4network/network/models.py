from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    following_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", blank=True)
