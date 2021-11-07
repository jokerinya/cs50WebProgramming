from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    following_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", blank=True)

class Post(models.Model):
    creater = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=280, blank=False)
    liked_users = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Returns last post first
    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f"{self.content[:25]}.."  # first 25 chars and plus ".."
    
    def create_time(self):
        return self.created_at.strftime("%b %d %Y, %I:%M %p")