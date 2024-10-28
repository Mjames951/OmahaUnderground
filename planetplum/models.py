from django.db import models
from django.conf import settings
from django.utils.timezone import datetime
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class venue(models.Model):
    name = models.CharField(max_length = 30, unique=True)

    ageRange_choices = [('A', 'All Ages'), ('8', '18+'), ('9', '19+'), ('2', '21+')]
    ageRange = models.CharField(max_length=1, choices = ageRange_choices, default='A')

    image = models.ImageField(upload_to="venueimages/", null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name="Information", help_text="Information on the venue or things people should know.")
    dm = models.BooleanField(default=False, verbose_name="Ask a punk for the address", help_text="Check the box if the address isn't public knowledge.")
    def __str__(self):
        return self.name
    
class label(models.Model):
    name = models.CharField(max_length = 30, unique=True)
    color = ColorField(default='#FFFFFF')
    image = models.ImageField(upload_to="labelimages/", null=True, blank=True)
    description = models.TextField(null=True, blank=True, help_text="A description about the label")
    link = models.URLField(null=True, blank=True, help_text="Does the label have a website or main social media?")
    email = models.EmailField(null=True, blank=True, help_text="email for contacting the label")
    valid = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class band(models.Model):
    name = models.CharField(max_length=50, unique=True)
    picture = models.ImageField(upload_to="bandpfps/")
    description = models.TextField(blank=True, null=True)
    label = models.ForeignKey(label, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bands", blank=True)
    associates = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="associated", blank=True)
    valid = models.BooleanField(default=True, null=True, blank=True)
    def __str__(self):
        return self.name

class showVibe(models.Model):
    name = models.CharField(max_length=30)
    color = ColorField(default='#FFFFFF')

class show(models.Model):
    approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to="showposters/", verbose_name="Poster")
    name = models.CharField(max_length=45, verbose_name="Title")
    date = models.DateField(default=datetime.today)
    venue = models.ForeignKey('venue', on_delete=models.RESTRICT, help_text="what's the name of the show location? **DON'T PUT AN ADDRESS HERE**")
    bands = models.ManyToManyField(band, blank=True, verbose_name="Local Bands Playing:", help_text="(Not Required) choose which local bands are playing this show")
    class Meta:
        ordering = ["-date", "name"]
    def __str__(self):
        return f"{self.name}, {self.date}"
    
class forumpost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.TextField(verbose_name='Title')
    parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True)
    description = models.TextField(verbose_name='Content', blank=True, null=True)
    image = models.ImageField(upload_to="forumimages/", blank=True, null=True)
    
class contactrequest(models.Model):
    name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 50)
    message = models.TextField()

    def __str__(self):
        return self.name

class devlog(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    datetime = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return self.title

class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="userpfps/", blank=True, null=True)
    verified = models.BooleanField(blank=True, null=True)
    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        userprofile.objects.create(user=instance)
    instance.userprofile.save()