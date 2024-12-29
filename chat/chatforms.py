from django import forms
from .models import Post, Channel, ChannelSection

class ChannelPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text", "image"]

class ChannelSectionForm(forms.ModelForm):
    class Meta:
        model = ChannelSection
        fields = ['name']

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['section', 'name']