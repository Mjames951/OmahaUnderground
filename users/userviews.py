from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser
from .userforms import UserProfileForm, RegisterForm, UserColorsForm
from django.contrib.auth import authenticate, login
from django.core.files.base import ContentFile
from django.views import View
from planetplum.tools import imagehandler
import os
from django.conf import settings

def userProfile(request, username):
    try:
        displayUser = get_object_or_404(CustomUser, username=username)
    except CustomUser.DoesNotExist:
        return redirect('index')
    return render(request, 'users/userProfile.html', {
        "displayUser": displayUser,
        })

def editUserColors(request):
    print("wuddup")
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    profile = user.userprofile
    if request.method == "POST":
        form = UserColorsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('userProfile', user.username)
    form = UserColorsForm(instance=profile)
    return render(request, 'users/editUserColors.html', {
        "form": form
    })

class editUserProfile(View):
    def send(self, request, form):
        return render(request, 'users/editUserProfile.html', {
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

        #print(form.cleaned_data)

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
            OGpicture = form.cleaned_data['profile_picture']
            picture, temp_picture = imagehandler.CropPicture(OGpicture, 'pfp')
            if not picture or not temp_picture:
                good = False
                print(f"FORM ERRORS: {form.errors}")
                form.add_error(None, 'The uploaded file is not a valid image.')
            else:
                #save the picture to the imagefield location and then save the model instance
                try:
                    profile.picture.save(picture, ContentFile(temp_picture.read()), save=False)
                    profile.save()
                except:
                    good = False
                    form.add_error(None, 'Unable to save the uploaded file.')
    
        #if there are not form errors
        if good:
            return redirect('userProfile', user.username)
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
            return redirect('userProfile', user.username)
        return render(request, "registration/register.html", {"form": form})