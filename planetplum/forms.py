from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import label

class FeedbackForm(forms.Form):
    content = forms.CharField(label="Message ", max_length=200)

class BandSearchForm(forms.Form):
    label = forms.ModelMultipleChoiceField(required=False, queryset=label.objects.all())
    bandSearch = forms.CharField(label="Search ", max_length=50, required=False)

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password1", "password2"]