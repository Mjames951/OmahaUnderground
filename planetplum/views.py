from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *
import datetime
from django.views import View
from .tools import emailhandler as esender

# Create your views here.
def index(request):
    shows = Show.objects.filter(date__gte=datetime.date.today(), approved=True)
    announcements = Announcement.objects.all().order_by('-created_at')[:3]
    return render(request, 'planetplum/index.html', {
        "shows": shows,
        "announcements": announcements,
    })

def showpage(request, showid):
    try: show = get_object_or_404(Show, id=showid)
    except: return redirect("index")
    return render(request, "planetplum/showpage.html",{
        "show": show,
    })

class shows(View):
    def send(self, request, shows, searchForm):
        return render(request, 'planetplum/shows.html',{
            "shows": shows,
            "searchform": searchForm,
        })
    def get(self, request):
        shows = Show.objects.filter(approved=True)
        searchForm = GeneralSearchForm
        return self.send(request, shows, searchForm)
    def post(self, request):
        searchForm = GeneralSearchForm(request.POST)
        if searchForm.is_valid():
            showSearch = searchForm.cleaned_data['Search']
            shows = Show.objects.filter(approved=True)
            if showSearch: shows = shows.filter(name__icontains=showSearch)
            return self.send(request, shows, searchForm)
        else: return self.get(request)
    

def bandpage(request, bandname):
    try: band = get_object_or_404(Band, name=bandname)
    except: return redirect("bands")
    return render(request, 'planetplum/bandpage.html',{
        "band": band,
    })
    

class bands(View):
    def send(self, request, bands, searchForm):
        return render(request, 'planetplum/bands.html', {
            "bands": bands,
            "searchform": searchForm,
        })
    def get(self, request):
        bands = Band.objects.filter(approved=True)
        searchForm = BandSearchForm
        return self.send(request, bands, searchForm)
    def post(self, request):
        searchForm = BandSearchForm(request.POST)
        if searchForm.is_valid():
            labels = searchForm.cleaned_data['label']
            bandSearch = searchForm.cleaned_data['bandSearch']
            bands = Band.objects.filter(approved=True)
            if labels: bands = bands.filter(label__in=labels)
            if bandSearch: bands = bands.filter(name__icontains=bandSearch)
            return self.send(request, bands, searchForm)
        else: return self.get(request)

def labelpage(request, labelname):
    try: label = get_object_or_404(Label, name=labelname)
    except: return redirect("labels")
    return render(request, 'planetplum/labelpage.html',{
        "label": label,
    })

class labels(View):
    def send(self, request, labels, searchForm):
        return render(request, 'planetplum/labels.html',{
            "labels": labels,
            "searchform": searchForm,
        })
    def get(self, request):
        labels = Label.objects.filter(approved=True)
        searchForm = GeneralSearchForm
        return self.send(request, labels, searchForm)
    def post(self, request):
        searchForm = GeneralSearchForm(request.POST)
        if searchForm.is_valid():
            labelSearch = searchForm.cleaned_data['Search']
            labels = Label.objects.filter(approved=True)
            if labelSearch: labels = labels.filter(name__icontains=labelSearch)
            return self.send(request, labels, searchForm)
        else: return self.get(request)

def venuepage(request, venuename):
    try: venue = get_object_or_404(Venue, name=venuename)
    except: return redirect("venues")
    return render(request, 'planetplum/venuepage.html',{
        "venue": venue,
    })

class venues(View):
    def send(self, request, venues, searchForm):
        return render(request, "planetplum/venues.html",{
            "venues": venues,
            "searchform": searchForm
        })
    def get(self, request):
        venues = Venue.objects.all()
        searchForm = GeneralSearchForm
        return self.send(request, venues, searchForm)
    def post(self, request):
        searchForm = GeneralSearchForm(request.POST)
        if searchForm.is_valid():
            venueSearch = searchForm.cleaned_data['Search']
            venues = Venue.objects.all()
            if venueSearch: venues = venues.filter(name__icontains=venueSearch)
            return self.send(request, venues, searchForm)
        else: return self.get(request)

def about(request):
    return render(request, 'planetplum/about.html', context=None)

def feedback(request):
    submitted = False
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            user = request.user
            username = user.username
            email = user.email
            content = form.cleaned_data['content']

            # replace this with an email handler to email me the response
            esender.admin_alert("dm", f"{username}\n{email}\nsays: {content}")
            print(f"{username} at {email} says: {content}")

            form = FeedbackForm()
            submitted = True
    else: form = FeedbackForm()
    return render(request, "planetplum/feedback.html", {
        "form": form,
        "submitted": submitted,
    })