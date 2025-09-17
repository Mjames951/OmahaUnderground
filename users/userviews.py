from .models import CustomUser
from .userforms import UserProfileForm, RegisterForm, UserColorsForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.core.files.base import ContentFile
from django.views import View
from django.contrib.auth.decorators import login_required

from planetplum.tools import imagehandler

def userProfile(request, username):
    displayUser = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/userProfile.html', {
        "displayUser": displayUser,
        })

@login_required
def editUserColors(request):
    profile = request.user.userprofile
    if request.method == "POST":
        form = UserColorsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('userprofile', request.user.username)
    else: form = UserColorsForm(instance=profile)
    return render(request, 'users/editUserColors.html', {"form": form})

@login_required
def editUserProfile(request):
    if not request.method == 'POST':
        user = request.user
        first_name = user.first_name if user.first_name else None
        form = UserProfileForm(initial={
            'name': first_name,
            'username': user.username,
            'email': user.email,
            'description': user.userprofile.description,
        })
    else:
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
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
                        
            #if username has changed
            if form.cleaned_data['username']:
                username = form.cleaned_data["username"]
                if username != user.username:
                    try:
                        CustomUser.objects.get(username=username)
                        form.add_error(None, "Username is already taken :(")
                        good = False
                    except:
                        user.username = username
                        user.save()

            #if there is a profile picture in the form
            if form.cleaned_data['profile_picture']:
                picture, temp_picture = imagehandler.CropPicture(form.cleaned_data['profile_picture'], 'pfp')
                if not picture or not temp_picture:
                    good = False
                    print(f"FORM ERRORS: {form.errors}")
                    form.add_error(None, 'The uploaded file is not a valid image.')
                else:
                    #save the picture to the imagefield location and then save the model instance
                    try:
                        profile.image.save(picture, ContentFile(temp_picture.read()), save=False)
                        profile.save()
                    except:
                        good = False
                        form.add_error(None, 'Unable to save the uploaded file.')
        
            #if user has a description
            if form.cleaned_data['description']:
                if form.cleaned_data['description'] != user.userprofile.description:
                    try:
                        user.userprofile.description = form.cleaned_data['description']
                        user.userprofile.save()
                    except:
                        good = False

            #if there are not form errors
            if good:
                return redirect('userprofile', user.username)
            
    return render(request, 'users/editUserProfile.html', {
            "form": form,
        })
        
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)  
            return redirect('userprofile', user.username)
    else: form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})