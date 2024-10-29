from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *
import datetime
from django.views import View
from django.core.files.base import ContentFile
from PIL import Image



# Create your views here.
def index(request):
    context = None
    return render(request, 'planetplum/index.html', context=context)

class bands(View):
    def send(self, request, bands, form):
        return render(request, 'planetplum/bands.html', {
            "bands": bands,
            "searchform": form,
        })
    def get(self, request):
        bands = band.objects.all()
        form = BandSearchForm
        return self.send(request, bands, form)
    def post(self, request):
        form = BandSearchForm(request.POST)
        if form.is_valid():
            labels = form.cleaned_data['label']
            bandSearch = form.cleaned_data['bandSearch']
            bands = band.objects.all()
            if labels: bands = bands.filter(label__in=labels)
            if bandSearch: bands = bands.filter(name__startswith=bandSearch)
            return self.send(request, bands, form)
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
            print(f"{username} at {email} says: {content}")

            form = FeedbackForm()
            submitted = True
    else:
        form = FeedbackForm()
    return render(request, "planetplum/feedback.html", {
        "form": form,
        "submitted": submitted,
    })

#profile picture dimension
ppd = 500
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if 'profile_picture' in request.FILES:
                profile = user.userprofile
                ogpicture = form.cleaned_data['profile_picture']
                picture = Image.open(ogpicture)

                print(picture.size)
                (width, height) = picture.size
                minside = min(width, height)
                picture = picture.crop(((width - minside) // 2,(height - minside) // 2,(width + minside) // 2,(height + minside) // 2))
                picture = picture.resize((ppd, ppd), Image.LANCZOS)

                print(picture.size)
                picture_name = user.username + ogpicture.name
                image_bytes = ContentFile(picture.tobytes())
                profile.picture.save(picture_name, image_bytes)
                profile.save()
            return redirect('login')
        return render(request, "registration/register.html", {"form": form})
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})