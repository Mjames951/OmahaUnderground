from django.db import models
from django.conf import settings

class ChannelSection(models.Model):
    name = models.CharField(max_length=50, verbose_name="Channel Section Name")
    def __str__(self):
        return self.name

class Channel(models.Model):
    section = models.ForeignKey(ChannelSection, on_delete=models.SET_DEFAULT, default=1)
    name = models.CharField(max_length=50, verbose_name="Channel Name")
    def __str__(self):
        return f"{self.section}: {self.name}"

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reply")
    channel = models.ForeignKey(Channel, on_delete=models.SET_DEFAULT, default=1)
    text = models.TextField(verbose_name='Message', blank=True, null=True)
    image = models.ImageField(upload_to="chatimages/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.timestamp}, {self.user.username} in {self.channel.section.name}:{self.channel.name} says: {self.text}"

class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.id


