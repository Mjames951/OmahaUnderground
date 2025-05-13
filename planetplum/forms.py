from django import forms
from users.userforms import UserCreationForm
from users.models import CustomUser
from .models import Label, Band, Show, Venue, Announcement, CommunityLink, CommunitySection

class FeedbackForm(forms.Form):
    content = forms.CharField(max_length=100)

class BandSearchForm(forms.Form):
    #label = forms.ModelMultipleChoiceField(required=False, queryset=Label.objects.filter(approved=True))
    bandSearch = forms.CharField(label="Search ", max_length=50, required=False)

class ShowSearchForm(forms.Form):
    lowerRange = forms.DateField(required=False, label="Lower Date Range")
    upperRange = forms.DateField(required=False, label="Upper Date Range")

class GeneralSearchForm(forms.Form):
    Search = forms.CharField(label="Search ", max_length=50, required=False)


class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['name', 'image', 'description', 'label', 'email']
        labels = {
            'name': 'Band Name',
            'image': 'Profile Picture',
        }
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
        labels = {
            'name': 'Label Name',
            'image': 'Profile Picture',
            'link': 'External Link (site/social)'
        }
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
    venueChoices = list(Venue.objects.all().values_list('id', 'name'))
    venueChoices.insert(0, ('', '-- select venue --'))
    venueChoices.append(('1000', '-- Other Venue --'))

    venue = forms.ChoiceField(choices=venueChoices)

    field_order = ['image', 'date', 'venue', 'name', 'price', 'pwyc', 'time']
    class Meta:
        model = Show 
        fields = ['image', 'date', 'name', 'price', 'pwyc', 'time']

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [ 'name', 'ageRange', 'dm', 'image', 'description']
        labels = {
            'name': 'Venue Name',
            'ageRange': 'Age Range Allowed',
            'dm': 'Ask a Punk for Address?',
            'image': 'Venue Image',
        }
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
    
class SubVenueForm(forms.Form):
    ageChoices = Venue.ageRange_choices

    name = forms.CharField(label='venue name',max_length=30, required=False)
    ageRange = forms.ChoiceField(label='age range',choices=ageChoices, required=False)
    dm = forms.BooleanField(required=False, label="private address")
    
    def is_valid(self):
        valid = super(SubVenueForm, self).is_valid()

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
        fields = ['name', 'link', 'image', 'description', 'section']
        labels = {
            'name': 'Organization/Site Name',
        }
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

        