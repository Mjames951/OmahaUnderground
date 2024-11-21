from django import forms
from users.userforms import UserCreationForm
from users.models import CustomUser
from .models import label, band

class FeedbackForm(forms.Form):
    content = forms.CharField(label="Message ", max_length=200)

class BandSearchForm(forms.Form):
    label = forms.ModelMultipleChoiceField(required=False, queryset=label.objects.all())
    bandSearch = forms.CharField(label="Search ", max_length=50, required=False)


class BandForm(forms.ModelForm):
    class Meta:
        model = band
        fields = ['name', 'picture', 'description', 'label', 'email', 'members', 'associates', 'valid']
