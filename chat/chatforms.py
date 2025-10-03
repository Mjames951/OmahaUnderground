from django import forms
from .models import Post, Root, Topic

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text", "image"]

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']

class RootForm(forms.ModelForm):
    class Meta:
        model = Root
        fields = ['topic', 'name']

    def is_valid(self):
        valid = super(RootForm, self).is_valid()
        
        invalidChars = [ '/' ]

        try: 
            if any([c in self.cleaned_data.get('name') for c in invalidChars]):
                self.add_error('name', 'no slashes in your name, it messes with the url patterns')
                valid = False
        except:
            valid = False

        return valid