from django import forms
from .models import post, channel, channelSection

class ChannelPostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ["text", "image"]

class ChannelSectionForm(forms.ModelForm):
    class Meta:
        model = channelSection
        fields = ['name']

class ChannelForm(forms.ModelForm):
    class Meta:
        model = channel
        fields = ['section', 'name']