from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *
import datetime
from django.views import View
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

from django.contrib.auth import authenticate, login

from users.models import CustomUser



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

def userProfile(request, username):
    try:
        displayUser = get_object_or_404(CustomUser, username=username)
    except CustomUser.DoesNotExist:
        return redirect('index')
    return render(request, 'planetplum/userProfile.html', {
        "displayUser": displayUser,
        })
    

#profile picture dimension
ppd = 500
class editUserProfile(View):
    def send(self, request, form):
        return render(request, 'registration/editUserProfile.html', {
            "form": form,
        })
    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user

        if user.first_name:
            first_name = user.first_name
        else: first_name = None

        form = UserProfileForm(initial={
            'name': first_name,
            'username': user.username,
            'email': user.email
            })
        
        return self.send(request, form)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = UserProfileForm(request.POST, request.FILES)

        #if form is invalid then resubmit
        valid = form.is_valid()
        if not valid:
            return self.send(request, form)
        user = request.user
        profile = user.userprofile
        good = True

        #if first_name has changed
        if form.cleaned_data['name']:
            if form.cleaned_data['name'] != user.first_name:
                try:
                    user.first_name = form.cleaned_data['name']
                    user.save()
                except:
                    good = False

        #if email has changed
        if form.cleaned_data['email']:
            email = form.cleaned_data['email']
            if email != user.email:
                try:
                    get_object_or_404(CustomUser, email=email)
                except:
                    #no user found so good to save
                    user.email = email
                    user.userprofile.verified = False
                    user.save()
                else:
                    form.add_error(None, "an account with that email already exists")
                    good = False
                    
        #if username has changed
        if form.cleaned_data['username']:
            username = form.cleaned_data["username"]
            if username != user.username:
                try:
                    get_object_or_404(CustomUser, username=username)
                except:
                    user.username = username
                    user.save()
                else:
                    form.add_error(None, "Username is already taken :(")
                    good = False

        #if there is a profile picture in the form
        if form.cleaned_data['profile_picture']:
            try: 
                OGpicture = form.cleaned_data['profile_picture']
                picture = Image.open(OGpicture)
                picture.verify()
                #reopen due to verify pointer at end of file
                picture = Image.open(OGpicture)

                #convert png to RGB
                if picture.mode in ("RGBA", "LA", "P"):
                    picture = picture.convert("RGB")

                #crop then resize the image with antialiazing optimizer (LANCZOS)
                (width, height) = picture.size
                minside = min(width, height)
                picture = picture.crop(((width - minside) // 2,(height - minside) // 2,(width + minside) // 2,(height + minside) // 2))
                picture = picture.resize((ppd, ppd), Image.LANCZOS)

                #Create a new picture file to be saved as the image
                temp_picture = BytesIO()
                picture.save(temp_picture, format="JPEG", quality=70, optimize=True)
                temp_picture.seek(0)
                original_name, _ = OGpicture.name.lower().split(".")
                picture = f"{original_name}.jpg"

                #save the picture to the imagefield location and then save the model instance
                profile.picture.save(picture, ContentFile(temp_picture.read()), save=False)
                profile.save()
                return redirect('userProfile', user.username)
                    
            except:
                good = False
                print(f"FORM ERRORS: {form.error_messages} {form.errors}")
                form.add_error(None, 'The uploaded file is not a valid image.')
        
        #if there are not form errors
        if good:
            return redirect('userProfile', request.user.username)
        
        #if there are form errors
        return self.send(request, form)
        

def register(request):
    if not request.method == "POST":
        form = RegisterForm()
        return render(request, "registration/register.html", {"form": form})
    #POST request:
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)  
            return redirect('userProfile')
        return render(request, "registration/register.html", {"form": form})