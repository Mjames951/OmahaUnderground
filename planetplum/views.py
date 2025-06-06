from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *
from .tools.timehandler import currentDate
from django.views import View
from .tools import emailhandler as esender
from .tools.userhandler import ConfirmUser
from django.db.models.functions import Lower

# Create your views here.
def index(request):
    todayShows = Show.objects.filter(date=currentDate(), approved=True)
    nextShows = Show.objects.filter(date__gt=currentDate(), approved=True).order_by('date')[:4]
    shows = (todayShows | nextShows).reverse()
    announcements = Announcement.objects.all().order_by('-created_at')[:3]
    return render(request, 'planetplum/index.html', {
        "shows": shows,
        "announcements": announcements,
    })

def showpage(request, showid):
    try: show = get_object_or_404(Show, id=showid)
    except: return redirect("index")
    if ConfirmUser(request.user) or show.contributor == request.user: edit=True 
    else: edit=False
    return render(request, "explore/showpage.html",{
        "show": show,
        "edit": edit
    })

class shows(View):
    def send(self, request, shows, searchForm, text=False):
        return render(request, 'explore/shows.html',{
            "shows": shows,
            "searchform": searchForm,
            "text": text,
        })
    def get(self, request):
        shows = Show.objects.filter(approved=True, date__gte=currentDate()).reverse()
        now = currentDate()
        searchForm = ShowSearchForm(initial={'lowerRange': str(now)})
        return self.send(request, shows, searchForm)
    def post(self, request):
        searchForm = ShowSearchForm(request.POST)
        if searchForm.is_valid():
            print(searchForm.cleaned_data)
            cleanData = searchForm.cleaned_data
            lowerDate = cleanData['lowerRange']
            upperDate = cleanData['upperRange']
            text = cleanData['text']

            shows = Show.objects.filter(approved=True).reverse()
            if lowerDate: shows = shows.filter(date__gte=lowerDate)
            if upperDate: shows = shows.filter(date__lte=upperDate)

            return self.send(request, shows, searchForm, text=text)
        else: return self.get(request)
    

def bandpage(request, bandname):
    try: band = get_object_or_404(Band, name=bandname)
    except: return redirect("bands")
    if ConfirmUser(request.user, "band", band): edit=True
    else: edit=False
    return render(request, 'explore/bandpage.html',{
        "band": band,
        "edit": edit,
    })
    

class bands(View):
    def send(self, request, bands, searchForm):
        return render(request, 'explore/bands.html', {
            "bands": bands,
            "searchform": searchForm,
        })
    def get(self, request):
        bands = Band.objects.filter(approved=True).order_by('?')
        searchForm = BandSearchForm
        return self.send(request, bands, searchForm)
    def post(self, request):
        searchForm = BandSearchForm(request.POST)
        if searchForm.is_valid():
            #labels = searchForm.cleaned_data['label']
            bandSearch = searchForm.cleaned_data['bandSearch']
            bands = Band.objects.filter(approved=True).order_by(Lower('name'))
            #if labels: bands = bands.filter(label__in=labels)
            if bandSearch: bands = bands.filter(name__icontains=bandSearch)
            return self.send(request, bands, searchForm)
        else: return self.get(request)

def labelpage(request, labelname):
    try: label = get_object_or_404(Label, name=labelname)
    except: return redirect("labels")
    if ConfirmUser(request.user, "label", label): edit=True
    else: edit=False
    return render(request, 'explore/labelpage.html',{
        "label": label,
        "edit": edit,
    })

class labels(View):
    def send(self, request, labels, searchForm):
        return render(request, 'explore/labels.html',{
            "labels": labels,
            "searchform": searchForm,
        })
    def get(self, request):
        labels = Label.objects.filter(approved=True).order_by(Lower('name'))
        searchForm = GeneralSearchForm
        return self.send(request, labels, searchForm)
    def post(self, request):
        searchForm = GeneralSearchForm(request.POST)
        if searchForm.is_valid():
            labelSearch = searchForm.cleaned_data['Search']
            labels = Label.objects.filter(approved=True).order_by(Lower('name'))
            if labelSearch: labels = labels.filter(name__icontains=labelSearch)
            return self.send(request, labels, searchForm)
        else: return self.get(request)

def venuepage(request, venuename):
    try: venue = get_object_or_404(Venue, name=venuename)
    except: return redirect("venues")
    if ConfirmUser(request.user): edit=True
    else: edit=False
    return render(request, 'explore/venuepage.html',{
        "venue": venue,
        "edit": edit,
    })

class venues(View):
    def send(self, request, venues, searchForm):
        return render(request, "explore/venues.html",{
            "venues": venues,
            "searchform": searchForm
        })
    def get(self, request):
        venues = Venue.objects.all().order_by(Lower('name'))
        searchForm = GeneralSearchForm
        return self.send(request, venues, searchForm)
    def post(self, request):
        searchForm = GeneralSearchForm(request.POST)
        if searchForm.is_valid():
            venueSearch = searchForm.cleaned_data['Search']
            venues = Venue.objects.all().order_by(Lower('name'))
            if venueSearch: venues = venues.filter(name__icontains=venueSearch)
            return self.send(request, venues, searchForm)
        else: return self.get(request)

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

def announcements(request):
    annments = Announcement.objects.all().order_by('-created_at')
    return render(request, 'planetplum/announcements.html', {
        "announcements": annments,
    })