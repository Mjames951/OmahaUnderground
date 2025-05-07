from django.contrib.auth.models import AbstractUser
from django.db import models
from colorfield.fields import ColorField
from django.db.models.signals import post_save  # new
from django.dispatch import receiver  # new

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    admin = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    def is_admin(self):
        return self.admin or self.is_superuser
    

class UserProfile(models.Model):  # new
    user = models.OneToOneField("users.CustomUser",on_delete=models.CASCADE,)
    image = models.ImageField(upload_to="userpfps/", blank=True, null=True)
    primary = ColorField(default="#00A1D8")
    secondary = ColorField(default='#FFFFFF')
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    def save(self, *args, **kwargs):
        try:
            this = UserProfile.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(UserProfile, self).save(*args, **kwargs)

@receiver(post_save, sender=CustomUser)  # new
def create_or_update_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)