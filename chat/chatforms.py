from django import forms
from .models import post

class ChannelPostForm(forms.ModelForm):
    
    class Meta:
        model = post
        fields = ["text", "image"]