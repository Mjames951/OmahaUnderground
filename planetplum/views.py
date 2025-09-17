from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models.functions import Lower

from .models import *
from .forms import *
from .tools.timehandler import currentDate, datePlus
from .tools.userhandler import ConfirmUser
from .tools import emailhandler


# Create your views here.
def index(request):
    todayShows = Show.objects.filter(date=currentDate(), approved=True)
    nextShows = Show.objects.filter(date__gt=currentDate(), date__lte=datePlus(3),approved=True).order_by('date')
    if nextShows.count() < 3:
        nextShows = Show.objects.filter(date__gt=currentDate(), approved=True).order_by('date')[:4]
        shows = (nextShows | todayShows).reverse()
    else:
        shows = (nextShows | todayShows)
    announcements = Announcement.objects.all().order_by('-created_at')[:1]
    return render(request, 'planetplum/index.html', {
        "shows": shows,
        "announcements": announcements,
        "currentday": currentDate(),
    })

def showpage(request, showid):
    show = get_object_or_404(Show, id=showid)
    edit = True if ConfirmUser(request.user) or show.contributor == request.user else False
    return render(request, "explore/showpage.html",{
        "show": show,
        "edit": edit
    })

class shows(View):
    def send(self, request, shows, searchForm, textmode=False):
        return render(request, 'explore/shows.html',{
            "shows": shows,
            "searchform": searchForm,
            "text": textmode,
        })
    #yeah there has to be a way to make this simpler
    def get(self, request):
        now = currentDate()
        searchForm = ShowSearchForm(request.GET)
        if searchForm.is_valid():
            cleanData = searchForm.cleaned_data
            lowerDate = cleanData['lowerRange']
            if lowerDate == None:
                #searchForm = ShowSearchForm(initial={'lowerRange': str(now)})
                searchForm.initial['lowerRange'] = str(now)
                lowerDate = str(now)
            upperDate = cleanData['upperRange']
            textmode = cleanData['text']

            shows = Show.objects.filter(approved=True).reverse()
            shows = shows.filter(date__gte=lowerDate)
            if upperDate: shows = shows.filter(date__lte=upperDate)

            return self.send(request, shows, searchForm, textmode=textmode)
        shows = Show.objects.filter(approved=True, date__gte=currentDate()).reverse()
        return self.send(request, shows, searchForm)

def bandpage(request, bandname):
    band = get_object_or_404(Band, name=bandname)
    edit = True if ConfirmUser(request.user, 'band', band) else False
    return render(request, 'explore/bandpage.html',{
        "band": band,
        "edit": edit,
    })
    
def bands(request):
    bands = Band.objects.filter(approved=True).order_by('?')
    searchForm = BandSearchForm(request.GET)
    if searchForm.is_valid():
        #labels = searchForm.cleaned_data['label']
        bandSearch = searchForm.cleaned_data['bandSearch']
        #if labels: bands = bands.filter(label__in=labels)
        if bandSearch: 
            bands = Band.objects.filter(approved=True).order_by(Lower('name'))
            bands = bands.filter(name__icontains=bandSearch)
    return render(request, 'explore/bands.html', {
        "bands": bands,
        "searchform": searchForm,
    })

def labelpage(request, labelname):
    label = get_object_or_404(Label, name=labelname)
    edit = True if ConfirmUser(request.user, 'label', label) else False
    return render(request, 'explore/labelpage.html',{
        "label": label,
        "edit": edit,
    })

def labels(request):
    labels = Label.objects.filter(approved=True).order_by(Lower('name'))
    searchForm = GeneralSearchForm(request.GET)
    if searchForm.is_valid():
        labelSearch = searchForm.cleaned_data['Search']
        if labelSearch: labels = labels.filter(name__icontains=labelSearch)
    return render(request, 'explore/labels.html',{
        "labels": labels,
        "searchform": searchForm,
    })

def venuepage(request, venuename):
    venue = get_object_or_404(Venue, name=venuename)
    edit = True if ConfirmUser(request.user) else False
    shows = Show.objects.filter(venue=venue, date__gte=currentDate()).order_by('date')
    return render(request, 'explore/venuepage.html',{
        "venue": venue,
        "edit": edit,
        'shows': shows,
    })

def venues(request):
    venues = Venue.objects.filter(approved=True).order_by(Lower('name'))
    searchForm = GeneralSearchForm(request.GET)
    if searchForm.is_valid():
        venueSearch = searchForm.cleaned_data['Search']
        if venueSearch: venues = venues.filter(name__icontains=venueSearch)
    return render(request, "explore/venues.html",{
        "venues": venues,
        "searchform": searchForm
    })

def community(request):
    communityLinks = CommunityLink.objects.filter(approved=True).order_by('section')
    return render(request, 'planetplum/community.html', {
        "commlinks": communityLinks
    })

def about(request):
    return render(request, 'planetplum/about.html', context=None)

def feedback(request):
    submitted = False
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            username = request.user.username
            email = request.user.email
            content = form.cleaned_data['content']
            emailhandler.admin_alert("dm", f"{username}\n{email}\nsays: {content}")
            form = FeedbackForm()
            submitted = True
    else: form = FeedbackForm()
    return render(request, "planetplum/feedback.html", {
        "form": form,
        "submitted": submitted,
    })

def announcements(request):
    annments = Announcement.objects.all().order_by('-created_at')
    return render(request, 'planetplum/announcements.html', {
        "announcements": annments,
    })

def csrf_failure(request, reason=""):
    return redirect('login')