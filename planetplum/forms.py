from django import forms
from users.forms import UserCreationForm
from users.models import CustomUser
from .models import label

class FeedbackForm(forms.Form):
    content = forms.CharField(label="Message ", max_length=200)

class BandSearchForm(forms.Form):
    label = forms.ModelMultipleChoiceField(required=False, queryset=label.objects.all())
    bandSearch = forms.CharField(label="Search ", max_length=50, required=False)

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

class UserProfileForm(forms.Form):
    profile_picture = forms.ImageField(required=False)
    name = forms.CharField(max_length=70, required=False)
    
    class Meta:
        model = CustomUser
        fields = ["username", "email"]
