from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FeedbackForm(forms.Form):
    content = forms.CharField(label="Message ", max_length=200)

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password1", "password2"]