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

    def is_valid(self):
        valid = super(ChannelSectionForm, self).is_valid()
        
        invalidChars = [ '/' ]

        try: 
            if any([c in self.cleaned_data.get('name') for c in invalidChars]):
                self.add_error('name', 'no slashes in your name, it messes with the url patterns')
                valid = False
        except:
            valid = False

        return valid

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['section', 'name']

    def is_valid(self):
        valid = super(ChannelForm, self).is_valid()
        
        invalidChars = [ '/' ]

        try: 
            if any([c in self.cleaned_data.get('name') for c in invalidChars]):
                self.add_error('name', 'no slashes in your name, it messes with the url patterns')
                valid = False
        except:
            valid = False

        return valid