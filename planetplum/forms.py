from django import forms
from django.db.models.functions import Lower
from django.contrib.sites.models import Site

import re

from .models import Label, Band, Show, Venue, Announcement, CommunityLink, BandLink, CommunitySection
from .tools import embedder

class FeedbackForm(forms.Form):
    content = forms.CharField(max_length=100)

class BandSearchForm(forms.Form):
    #label = forms.ModelMultipleChoiceField(required=False, queryset=Label.objects.filter(approved=True))
    bandSearch = forms.CharField(label="Search ", max_length=50, required=False)

class ShowSearchForm(forms.Form):
    lowerRange = forms.DateField(required=False, label="Lower Date Range")
    upperRange = forms.DateField(required=False, label="Upper Date Range")
    text = forms.BooleanField(required=False, label="text mode")

class GeneralSearchForm(forms.Form):
    Search = forms.CharField(label="Search ", max_length=50, required=False)


class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['name', 'image', 'description', 'label', 'email', 'song']
        labels = {
            'name': 'Band Name',
            'image': 'Profile Picture',
            'email': 'Email (for contact)',
            'song': 'Featured Song! (Paste the BANDCAMP URL)',
        }
    def is_valid(self):
        valid = super(BandForm, self).is_valid()
        
        invalidNames = ['explore', 'shows', 'feedback', 'about', 'labels', 'venues', 'bands', 'admin', 'contribute', 'user', 'accounts', 'chat', 'announcements']
        invalidChars = [ '/' ]

        try: 
            #band name
            print("VALIDATING")
            if self.cleaned_data.get('name') in invalidNames:
                self.add_error('name', 'Sorry dude, your band name cannot be that. It will break the site')
                valid = False
            if any([c in self.cleaned_data.get('name') for c in invalidChars]):
                self.add_error('name', 'no slashes in your name, it messes with the url patterns')
                valid = False
            print("PASSED NAME CHECK")

            if self.cleaned_data.get('song') is not None:
                songURL = self.cleaned_data.get('song')
                regexResult = re.search('bandcamp.com/((track)|(album))/.+', songURL)
                if regexResult == None:
                    self.add_error('song', 'we only accept bandcamp URLs! Also check that you have the direct URL of a track or album. We take care of making the embed.')
                    valid = False
                try:
                    embedder.bandcamp(songURL)
                except:
                    self.add_error('song', 'that bandcamp URL does not exist! Maybe you misspelled something')
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
    venue = forms.ModelChoiceField(queryset=Venue.objects.filter(approved=True).order_by(Lower('name')))

    field_order = ['image', 'date', 'venue', 'name', 'price', 'pwyc', 'time', 'ticketlink']

    class Meta:
        model = Show 
        fields = ['image', 'date', 'name', 'price', 'pwyc', 'time', 'ticketlink']
        labels = {'ticketlink': 'Ticket Link',}

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [ 'name', 'ageRange', 'dm', 'image', 'description', 'map']
        labels = {
            'name': 'Venue Name',
            'ageRange': 'Age Range Allowed',
            'dm': 'Ask a Punk for Address?',
            'image': 'Venue Image',
            'map': 'Google Maps Embedded URL',
        }
    def is_valid(self):
        valid = super(VenueForm, self).is_valid()

        invalidChars = [ '/' ]

        try: 
            if any([c in self.cleaned_data.get('name') for c in invalidChars]):
                self.add_error('name', 'no slashes in your name, it messes with the url patterns')
                valid = False
            if self.cleaned_data.get('map'):
                print(self.cleaned_data.get('map'))
                map = self.cleaned_data.get('map')
                regexResult = re.search('<iframe src="https://www.google.com/maps/embed?.+</iframe>', map)
                print(regexResult)
                if regexResult == None:
                    self.add_error('map', 'make sure that it is an embed link and not just the URL of the location')
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
        fields = ['name', 'link', 'image', 'description', 'section', 'approved']
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

class BandLinkForm(forms.ModelForm):
    class Meta:
        model = BandLink
        fields = ['name', 'link']
        labels = {
            'name': 'link name',
            'link': 'URL / link'
        }


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['domain', 'name']
        