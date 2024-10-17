from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    profile_picture = forms.ImageField(help_text="Not Required, and can be added/changed later.")

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password1", "password2"]