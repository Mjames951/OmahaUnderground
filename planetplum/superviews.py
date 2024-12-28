from django.shortcuts import render, get_object_or_404, redirect
from .tools import imagehandler
import os 
from django.core.files.base import ContentFile

from .models import *
from .forms import *
import datetime

from django.views import View

def check(request):
    if not request.user.is_superuser:
        return redirect('index')

def superuser(request):
    check(request)
    return render(request, "superuser/superuser.html")

def addShow(request):
    check(request)
    if request.method == "POST":
        showform = ShowForm(request.POST, request.FILES)
        if showform.is_valid():
            showform.save()
            
            #maybe change to the bands new page?
            return redirect("superuser")
    else:
        showform = ShowForm()
    return render(request, "superuser/add/addshow.html",{
        "form": showform,
    })

def addBand(request):
    check(request)
    if request.method == "POST":
        bandform = BandForm(request.POST, request.FILES)
        if bandform.is_valid():
            OGpicture = bandform.cleaned_data['picture']
            picture, temp_picture = imagehandler.CropPicture(OGpicture, 'band')
            if not picture or not temp_picture:
                bandform.add_error(None, 'The uploaded file is not a valid image.')
            else:
                newBand = bandform.save(commit=False)
                try: #to save the image
                    newBand.picture.save(picture, ContentFile(temp_picture.read()), save=False)
                    newBand.save()
                except:
                    bandform.add_error(None, 'Unable to save the uploaded file.')
                    newBand.delete()

                #maybe change to the bands new page?
                return redirect("superuser")
    else:
        bandform = BandForm()
    return render(request, "superuser/add/addband.html",{
        "form": bandform,
    })

def editBand(request, bandname):
    check(request)
    def reload(b):
        bandform = BandForm(instance=b)
        return render(request, "superuser/editband.html",{
            "form": bandform,
        })
    try: b = get_object_or_404(band, name=bandname)
    except: return redirect("index")
    if not request.method == "POST":
        return reload(b)
    bandform = BandForm(request.POST, request.FILES, instance=b)
    if not bandform.is_valid():
        return reload(b)
    if bandform.cleaned_data['picture']:
        OGpicture = bandform.cleaned_data['picture']
        picture, temp_picture = imagehandler.CropPicture(OGpicture, 'band')
        if not picture or not temp_picture:
            bandform.add_error(None, 'The uploaded file is not a valid image.')
            return reload(b)
        try: #to save the image
            b.picture.save(picture, ContentFile(temp_picture.read()), save=False)
            b.save()
        except:
            bandform.add_error(None, 'Unable to save the uploaded file.')
            return reload(b) 
    bandform.save()
    return redirect("bandpage", bandname=bandname)

def addLabel(request):
    check(request)
    if request.method == "POST":
        labelform = LabelForm(request.POST, request.FILES)
        if labelform.is_valid():
            if not labelform.cleaned_data['image']:
                labelform.save()
                return redirect("superuser") #change to label page
            OGimage = labelform.cleaned_data['image']
            picture, temp_picture = imagehandler.CropPicture(OGimage, 'band')
            if not picture or not temp_picture:
                labelform.add_error(None, 'uploaded file is not valid image')
            else:
                newLabel = labelform.save(commit=False)
                try: #to save the image
                    newLabel.image.save(picture, ContentFile(temp_picture.read()), save=False)
                    newLabel.save()
                except:
                    labelform.add_error(None, "unable to save image")
                    newLabel.delete()
            
            return redirect("labelpage", labelname=newLabel.name)
    else:
        labelform = LabelForm()
    return render(request, "superuser/add/addlabel.html",{
        "form": labelform,
    })

def editLabel(request, labelname):
    check(request)
    def reload(l):
        labelform = LabelForm(instance=l)
        return render(request, "superuser/editlabel.html",{
            "form": labelform
        })
    try: l = get_object_or_404(label, name=labelname)
    except: return redirect("index")
    if not request.method == "POST":
        return reload(l)
    labelform = LabelForm(request.POST, request.FILES, instance=l)
    if not labelform.is_valid():
        return reload(l)
    if labelform.cleaned_data['image']:
        OGpicture = labelform.cleaned_data['image']
        picture, temp_picture = imagehandler.CropPicture(OGpicture, 'band')
        if not picture or not temp_picture:
            labelform.add_error(None, 'uploaded file not valid image')
            return reload(l)
        try: #to save the image
            l.image.save(picture, ContentFile(temp_picture.read()), save=False)
            l.save
        except:
            labelform.add_error(None, 'unable to save image')
            return reload(l)
    labelform.save()
    return redirect("labelpage", labelname=labelname)
    