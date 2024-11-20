from django.db import models
from django.conf import settings

class channel(models.Model):
    name = models.CharField(verbose_name="Channel Name")

class post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.ForeignKey(channel, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Message', blank=True, null=True)
    image = models.ImageField(upload_to="chatimages/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class report(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)


