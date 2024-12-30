from django import forms
from users.userforms import UserCreationForm
from users.models import CustomUser
from .models import Label, Band, Show, Venue

class FeedbackForm(forms.Form):
    content = forms.CharField(label="Message ", max_length=200)

class BandSearchForm(forms.Form):
    label = forms.ModelMultipleChoiceField(required=False, queryset=Label.objects.all())
    bandSearch = forms.CharField(label="Search ", max_length=50, required=False)

class GeneralSearchForm(forms.Form):
    Search = forms.CharField(label="Search ", max_length=50, required=False)


class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['name', 'image', 'description', 'label', 'email', 'members', 'associates', 'valid']

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'image', 'description', 'color', 'link', 'email']

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show 
        fields = ['image', 'date', 'venue', 'name', 'bands']

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [ 'name', 'ageRange', 'dm', 'image', 'description']