from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'id']


class Listing(models.Model):
    creater = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.CharField(max_length=255, blank=True)
    categories = models.ManyToManyField(
        Category, related_name="listings", blank=True)
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.listing} - ${self.price}"


class Watching(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watching")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watching")
    watching = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.listing} - {self.watching}"


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented on {self.listing}"
    # Orders newest to pastest

    class Meta:
        ordering = ['-created_at', 'id']
