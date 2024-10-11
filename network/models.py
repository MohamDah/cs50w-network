from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class post(models.Model):
    poster = models.CharField(max_length=64)
    text = models.CharField(max_length=280)
    date = models.DateTimeField()

    def __str__(self):
        return f"post by: {self.poster} at: {self.date}"


class follow(models.Model):
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.following_user} follows {self.followed_user}"


class likes(models.Model):
    liked = models.ForeignKey(post, on_delete=models.CASCADE, related_name="likers")
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likeds")

    def __str__(self):
        return f"{self.liker.username} liked {self.liked}"