from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from .models import UserProfile
import colorfield


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

class UserProfileForm(forms.Form):
    profile_picture = forms.ImageField(required=False)
    name = forms.CharField(max_length=70, required=False)
    username = forms.CharField(max_length=50)
    email = forms.EmailField()

class UserColorsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["primary", "secondary"]