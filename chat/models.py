from django.db import models
from django.conf import settings
from django.urls import reverse

#TOPIC
class Topic(models.Model):
    name = models.CharField(max_length=50, verbose_name="Topic Name")
    def __str__(self):
        return self.name

#ROOT POST
class Root(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_DEFAULT, default=1, related_name="channel")
    name = models.CharField(max_length=50, verbose_name="Channel Name")
    def __str__(self):
        return f"{self.topic}: {self.name}"
    def get_absolute_url(self):
        return reverse('root', args=[self.name])

#REPLY
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    root = models.ForeignKey(Root, on_delete=models.SET_DEFAULT, default=1, related_name="replies")
    text = models.TextField(verbose_name='Message', blank=True, null=True)
    image = models.ImageField(upload_to="chatimages/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.timestamp}, {self.user.username} in {self.root.topic.name}:{self.Root.name} says: {self.text}"

class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    root = models.ForeignKey(Root, on_delete=models.CASCADE)
    def __str__(self):
        return self.id


