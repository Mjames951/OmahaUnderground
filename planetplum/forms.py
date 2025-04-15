from django import forms
from users.userforms import UserCreationForm
from users.models import CustomUser
from .models import Label, Band, Show, Venue, Announcement, CommunityLink, CommunitySection

class FeedbackForm(forms.Form):
    content = forms.CharField(label="Message ", max_length=200)

class BandSearchForm(forms.Form):
    label = forms.ModelMultipleChoiceField(required=False, queryset=Label.objects.filter(approved=True))
    bandSearch = forms.CharField(label="Search ", max_length=50, required=False)

class ShowSearchForm(forms.Form):
    pastShows = forms.BooleanField(required=False)
    lowerRange = forms.DateField(required=False)
    upperRange = forms.DateField(required=False)

class GeneralSearchForm(forms.Form):
    Search = forms.CharField(label="Search ", max_length=50, required=False)


class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['name', 'image', 'description', 'label', 'email']

    def is_valid(self):
        valid = super(BandForm, self).is_valid()
        
        invalidNames = ['explore', 'shows', 'feedback', 'about', 'labels', 'venues', 'bands', 'admin', 'contribute', 'user', 'accounts', 'chat']
        invalidChars = [ '/' ]

        try: 
            if self.cleaned_data.get('name') in invalidNames:
                self.add_error('name', 'Sorry dude, your band name cannot be that. It will break the site')
                valid = False
            if any([c in self.cleaned_data.get('name') for c in invalidChars]):
                self.add_error('name', 'no slashes in your name, it messes with the url patterns')
                valid = False
        except:
            valid = False

        return valid

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'image', 'description', 'color', 'link', 'email']

    def is_valid(self):
        valid = super(LabelForm, self).is_valid()

        invalidChars = [ '/' ]

        try: 
            if any([c in self.cleaned_data.get('name') for c in invalidChars]):
                self.add_error('name', 'no slashes in the name, it messes with the url patterns')
                valid = False
        except:
            valid = False

        return valid

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show 
        fields = ['image', 'date', 'venue', 'name', 'price', 'pwyc', 'time']

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [ 'name', 'ageRange', 'dm', 'image', 'description']

    def is_valid(self):
        valid = super(VenueForm, self).is_valid()

        invalidChars = [ '/' ]

        try: 
            if any([c in self.cleaned_data.get('name') for c in invalidChars]):
                self.add_error('name', 'no slashes in your name, it messes with the url patterns')
                valid = False
        except:
            valid = False

        return valid
    
class CommlinkForm(forms.ModelForm):
    class Meta:
        model = CommunityLink
        fields = ['name', 'link', 'image', 'description', 'section', 'approved']

    def is_valid(self):
        valid = super(CommlinkForm, self).is_valid()

        invalidChars = [ '/' ]

        try: 
            if any([c in self.cleaned_data.get('name') for c in invalidChars]):
                self.add_error('name', 'no slashes in the name, it messes with the url patterns')
                valid = False
        except:
            valid = False

        return valid

class CommsecForm(forms.ModelForm):
    class Meta:
        model = CommunitySection
        fields = ['name']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [ 'name', 'image', 'banner', 'description' ]

        