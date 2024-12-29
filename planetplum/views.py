from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *
import datetime
from django.views import View
from django.core.files.base import ContentFile
from .tools import emailhandler as esender

# Create your views here.
def index(request):
    context = None
    return render(request, 'planetplum/index.html', context=context)

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
        bands = Band.objects.all()
        searchForm = BandSearchForm
        return self.send(request, bands, searchForm)
    def post(self, request):
        searchForm = BandSearchForm(request.POST)
        if searchForm.is_valid():
            labels = searchForm.cleaned_data['label']
            bandSearch = searchForm.cleaned_data['bandSearch']
            bands = Band.objects.all()
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
        labels = Label.objects.all()
        searchForm = LabelSearchForm
        return self.send(request, labels, searchForm)
    def post(self, request):
        searchForm = LabelSearchForm(request.POST)
        if searchForm.is_valid():
            labelSearch = searchForm.cleaned_data['labelSearch']
            labels = Label.objects.all()
            if labels: labels = labels.filter(label__in=labels)
            if labelSearch: labels = labels.filter(name__icontains=labelSearch)
            return self.send(request, labels, searchForm)
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
    else:
        form = FeedbackForm()
    return render(request, "planetplum/feedback.html", {
        "form": form,
        "submitted": submitted,
    })