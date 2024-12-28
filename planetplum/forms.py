from django import forms
from users.userforms import UserCreationForm
from users.models import CustomUser
from .models import label, band, show

class FeedbackForm(forms.Form):
    content = forms.CharField(label="Message ", max_length=200)

class BandSearchForm(forms.Form):
    label = forms.ModelMultipleChoiceField(required=False, queryset=label.objects.all())
    bandSearch = forms.CharField(label="Search ", max_length=50, required=False)

class LabelSearchForm(forms.Form):
    labelSearch = forms.CharField(label="Search ", max_length=50, required=False)


class BandForm(forms.ModelForm):
    class Meta:
        model = band
        fields = ['name', 'picture', 'description', 'label', 'email', 'members', 'associates', 'valid']

class LabelForm(forms.ModelForm):
    class Meta:
        model = label
        fields = ['name', 'image', 'description', 'link', 'email']

class ShowForm(forms.ModelForm):
    class Meta:
        model = show 
        fields = ['image', 'date', 'venue', 'name', 'bands']