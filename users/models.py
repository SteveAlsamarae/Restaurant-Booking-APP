from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from django_resized import ResizedImageField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = ResizedImageField(
        size=[300, 300],
        crop=["middle", "center"],
        upload_to="avatars",
        default="default.jpg",
        quality=70,
        keep_meta=False,
        verbose_name="avatar",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

    # delete user's avater when user is deleted
    def delete(self, *args, **kwargs):
        self.avatar.delete()

        return super(UserProfile, self).delete(*args, **kwargs)


class RestaurantAdmin(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="restaurant_admin"
    )
    avatar = ResizedImageField(
        size=[300, 300],
        crop=["middle", "center"],
        upload_to="avatars",
        default="restaurant_admin.jpg",
        quality=80,
        keep_meta=False,
        verbose_name="avatar",
    )
    role = models.CharField(max_length=10, default="restaurant_admin")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s restaurant admin"

    # delete user's avater when user is deleted
    def delete(self, *args, **kwargs):
        self.avatar.delete()

        return super(RestaurantAdmin, self).delete(*args, **kwargs)
