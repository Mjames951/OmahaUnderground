from django.contrib.auth.models import AbstractUser
from django.db import models
from colorfield.fields import ColorField
from django.db.models.signals import post_save  # new
from django.dispatch import receiver  # new

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username} :\t{self.email}"
    

class UserProfile(models.Model):  # new
    user = models.OneToOneField("users.CustomUser",on_delete=models.CASCADE,)
    picture = models.ImageField(upload_to="userpfps/", blank=True, null=True)
    primary = ColorField(default='#FFFFFF')
    secondary = ColorField(default='#FFFFFF')
    verified = models.BooleanField(default=False)


    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

@receiver(post_save, sender=CustomUser)  # new
def create_or_update_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)