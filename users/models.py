from django.contrib.auth.models import AbstractUser
from django.db import models
from colorfield.fields import ColorField
from django.db.models.signals import post_save  # new
from django.dispatch import receiver  # new


# WARNING WARNING WARNING WARNING WARNING
# IF THIS FILE GETS CHANGED FOR ANY REASON THEN IT MUST BE COPIED INTO THE PLANET SHOP USERS MODEL.PY TO AVOID THE DATABASE FROM EXPLODING

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    admin = models.BooleanField(default=False)
    trusted = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    def is_admin(self):
        return self.admin or self.is_superuser
    def is_trusted(self):
        return self.trusted or self.admin or self.is_superuser
    
# WARNING WARNING WARNING WARNING WARNING

class UserProfile(models.Model):  # new
    user = models.OneToOneField("users.CustomUser",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="userpfps/", blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    primary = ColorField(default="#6666ff")
    secondary = ColorField(default='#FFFFFF')

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

# WARNING WARNING WARNING WARNING WARNING

@receiver(post_save, sender=CustomUser)  # new
def create_or_update_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)