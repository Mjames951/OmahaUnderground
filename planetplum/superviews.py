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
    def reload():
        bandform = BandForm(instance=b)
        return render(request, "superuser/editband.html",{
            "form": bandform,
        })
    try: b = get_object_or_404(band, name=bandname)
    except: return redirect("index")
    if not request.method == "POST":
        return reload()
    bandform = BandForm(request.POST, request.FILES, instance=b)
    if not bandform.is_valid():
        return reload()
    if bandform.cleaned_data['picture']:
        OGpicture = bandform.cleaned_data['picture']
        picture, temp_picture = imagehandler.CropPicture(OGpicture, 'band')
        if not picture or not temp_picture:
            bandform.add_error(None, 'The uploaded file is not a valid image.')
            return reload()
        try: #to save the image
            b.picture.save(picture, ContentFile(temp_picture.read()), save=False)
            b.save()
        except:
            bandform.add_error(None, 'Unable to save the uploaded file.')
            return reload() 
    bandform.save()
    return redirect("bandpage", bandname=bandname)

def addLabel(request):
    check(request)
    if request.method == "POST":
        labelform = LabelForm(request.POST, request.FILES)
        if labelform.is_valid():
            labelform.save()
            
            #maybe change to the bands new page?
            return redirect("superuser")
    else:
        labelform = LabelForm()
    return render(request, "superuser/add/addlabel.html",{
        "form": labelform,
    })

def editLabel(request, labelname):
    check(request)
    try: l = get_object_or_404(label, name=labelname)
    except: return redirect("index")
    if request.method == "POST":
        labelform = LabelForm(request.POST, request.FILES, instance=l)
        if labelform.is_valid():
            labelform.save()
            
            #maybe change to the bands new page?
            return redirect("labelpage", labelname=labelname)
    else:
        labelform = LabelForm(instance=l)
    return render(request, "superuser/editlabel.html",{
        "form": labelform,
    })
    