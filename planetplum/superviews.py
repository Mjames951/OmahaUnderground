from django.shortcuts import render, get_object_or_404, redirect
from .tools import imagehandler
import os 
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
import datetime

from django.views import View

#(type of model, modelform being passed, 
#   image handler function name (str) for resizing, 
#   modelinstance if replacing/editing)
def addImage(form, func, modelInstance=None):
    Image = form.cleaned_data['image']
    imageName, newImage = imagehandler.CropPicture(Image, func)
    if not imageName or not newImage:
        form.add_error(None, 'The uploaded file is not a valid image')
        return False
    try: #to save the image
        if not modelInstance: modelInstance = form.save(commit=False)
        modelInstance.image.save(imageName, ContentFile(newImage.read()), save=False)
        return modelInstance
    except:
        form.add_error(None, "Unable to save the uploaded file.")
        modelInstance.delete()
        return None
    
def contribute(request):
    return render(request, 'planetplum/contribute.html', {

    })


#main superuser page
def superuser(request):
    if not request.user.is_superuser: return redirect('index')
    shows = Show.objects.filter(approved=False)
    bands = Band.objects.filter(approved=False)
    labels = Label.objects.filter(approved=False)
    return render(request, "planetplum/superuser.html", {
        "shows": shows,
        "bands": bands,
        "labels": labels,
    })


#replace this eventually with @user_passes_test(our defined function, redirect_field_name)
#have the test check if the user is super, or owner of post/is labelmate or whatever

@login_required
def addShow(request):
    if request.method == "POST":
        showForm = ShowForm(request.POST, request.FILES)
        if showForm.is_valid():
            show = addImage(showForm, 'show') 
            if request.user.is_superuser: show.approved = True
            show.save()
            #change to the new show page
            return redirect("showpage", showid = show.id)
    #GET method or invalid form
    else: showForm = ShowForm()
    return render(request, "contribute/add/addshow.html",{
        "form": showForm,
    })

def editShow(request, showid):
    if not request.user.is_superuser: redirect("index")
    try: show = get_object_or_404(Show, id=showid)
    except: return redirect("index")
    if request.method == "POST":
        showForm = ShowForm(request.POST, request.FILES, instance=show)
        if showForm.is_valid():
            if showForm.cleaned_data['image']:
                show = addImage(showForm, 'show', modelInstance=show)
                show.save()
            else:
                show = showForm.save()
            print(show.pwyc)
            print(showForm.cleaned_data)
            return redirect("showpage", showid=showid)
    #GET method or invalid form
    else: showForm = ShowForm(instance=show)
    return render(request, "contribute/edit/editshow.html",{
        "form": showForm
    })

@login_required
def addBand(request):
    if request.method == "POST":
        bandForm = BandForm(request.POST, request.FILES)
        if bandForm.is_valid():
            band = addImage(bandForm, 'band')
            if request.user.is_superuser: band.approved = True
            band.save()
            if band:
                return redirect("bandpage", bandname=band.name)
    #GET method or invalid form
    else: bandForm = BandForm()
    return render(request, "contribute/add/addband.html",{
        "form": bandForm,
    })


def editBand(request, bandname):
    if not request.user.is_superuser: return redirect('index')
    try: band = get_object_or_404(Band, name=bandname)
    except: return redirect("index")
    if request.method == "POST":
        bandForm = BandForm(request.POST, request.FILES, instance=band)
        if bandForm.is_valid():
            if bandForm.cleaned_data['image']:
                band = addImage(bandForm, 'band', modelInstance=band)
                band.save()
            else:
                bandForm.save()
            return redirect("bandpage", bandname=bandname)
    #GET method or invalid form
    else: bandForm = BandForm(instance=band)
    return render(request, "contribute/edit/editband.html",{
        "form": bandForm
    })

@login_required
def addLabel(request):
    if request.method == "POST":
        labelForm = LabelForm(request.POST, request.FILES)
        if labelForm.is_valid():
            if not labelForm.cleaned_data['image']:
                label = labelForm.save(commit=False)
            else: label = addImage(labelForm, 'band') #same size as band pfp 
            if request.user.is_superuser: label.approved = True
            label.save()
            return redirect("labelpage", labelname=label.name)
    #get method or invalid form
    else: labelForm = LabelForm()
    return render(request, "contribute/add/addlabel.html",{
        "form": labelForm,
    })

def editLabel(request, labelname):
    if not request.user.is_superuser: return redirect('index')
    try: label = get_object_or_404(Label, name=labelname)
    except: return redirect("index")
    if request.method == "POST":
        labelForm = LabelForm(request.POST, request.FILES, instance=label)
        if labelForm.is_valid():
            if labelForm.cleaned_data['image']:
                label = addImage(labelForm, 'band', modelInstance=label)
                label.save()
            else:
                labelForm.save()
            return redirect("labelpage", labelname=labelname)
    #GET method or invalid form
    else: labelForm = LabelForm(instance=label)
    return render(request, "contribute/edit/editlabel.html",{
        "form": labelForm
    })
    
@login_required
def addVenue(request):
    if request.method == "POST":
        venueForm = VenueForm(request.POST, request.FILES)
        if venueForm.is_valid():
            if not venueForm.cleaned_data['image']:
                venue = venueForm.save(commit=False)
            else: venue = addImage(venueForm, 'band') #same size as bandpfp
            venue.save()
            return redirect("venuepage", venuename=venue.name)
    #GET method or invalid form
    else: venueForm = VenueForm()
    return render(request, "contribute/add/addvenue.html",{
        "form": venueForm
    })

def editVenue(request, venuename):
    if not request.user.is_superuser: return redirect('index')
    try: venue = get_object_or_404(Venue, name=venuename)
    except: return redirect("index")
    if request.method == "POST":
        venueForm = VenueForm(request.POST, request.FILES, instance=venue)
        if venueForm.is_valid():
            if venueForm.cleaned_data['image']:
                venue = addImage(venueForm, 'band', modelInstance=venue)
                venue.save()
            else:
                venueForm.save()
            return redirect("venuepage", venuename=venuename)
    #GET method or invalid form
    else: venueForm = VenueForm(instance=venue)
    return render(request, "contribute/edit/editvenue.html",{
        "form": venueForm
    })

def addAnnouncement(request):
    if not request.user.is_superuser: return redirect("index")
    if request.method == "POST":
        announcementForm = AnnouncementForm(request.POST, request.FILES)
        if announcementForm.is_valid():
            if not announcementForm.cleaned_data['image']:
                announcement = announcementForm.save()
            else: 
                announcement = addImage(announcementForm, 'show')
                announcement.save()
            return redirect("index")
    else: announcementForm = AnnouncementForm()
    return render(request, "contribute/add/addannouncement.html",{
        "form": announcementForm,
    })

def editAnnouncement(request, announcementid):
    if not request.user.is_superuser: return redirect("index")
    try: announcement = get_object_or_404(Announcement, id=announcementid)
    except: return redirect("index")
    if request.method == 'POST':
        announcementForm = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if announcementForm.is_valid():
            if announcementForm.cleaned_data['image']:
                announcement = addImage(announcementForm, 'show', modelInstance=announcement)
                announcement.save()
            else:
                announcementForm.save()
            return redirect("index")
    else: announcementForm = AnnouncementForm(instance=announcement)
    return render(request, "contribute/edit/editannouncement.html", {
        "form": announcementForm
    })

@login_required
def addCommlink(request):
    if request.method == "POST":
        commlinkForm = CommlinkForm(request.POST, request.FILES)
        if commlinkForm.is_valid():
            if not commlinkForm.cleaned_data['image']:
                commlink = commlinkForm.save()
            else: 
                commlink = addImage(commlinkForm, 'show')
                commlink.save()
            return redirect("index")
    else: commlinkForm = CommlinkForm()
    return render(request, "contribute/add/addcommlink.html",{
        "form": commlinkForm,
    })


def approveShow(request, showid):
    if not request.user.is_superuser: return redirect("index")
    try: show = get_object_or_404(Show, id=showid)
    except: return redirect("index")
    show.approved = True
    show.save()
    return redirect("showpage", showid)

def approveBand(request, bandname):
    if not request.user.is_superuser: return redirect("index")
    try: band = get_object_or_404(Band, name=bandname)
    except: return redirect("index")
    band.approved = True
    band.save()
    return redirect("bandpage", bandname)
    
def approveLabel(request, labelname):
    if not request.user.is_superuser: return redirect("index")
    try: label = get_object_or_404(Label, name=labelname)
    except: return redirect("index")
    label.approved = True
    label.save()
    return redirect("labelpage", labelname)