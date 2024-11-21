from django.shortcuts import render, get_object_or_404, redirect

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

def addBand(request):
    check(request)
    if request.method == "POST":
        bandform = BandForm(request.POST, request.FILES)
        if bandform.is_valid:
            bandform.save()
            
            #maybe change to the bands new page?
            return redirect("superuser")
    else:
        bandform = BandForm()
    return render(request, "superuser/addband.html",{
        "form": bandform,
    })

def editBand(request, bandname):
    check(request)
    try: b = get_object_or_404(band, name=bandname)
    except: return redirect("index")
    if request.method == "POST":
        bandform = BandForm(request.POST, request.FILES, instance=b)
        if bandform.is_valid:
            bandform.save()
            
            #maybe change to the bands new page?
            return redirect("superuser")
    else:
        bandform = BandForm(instance=b)
    return render(request, "superuser/addband.html",{
        "form": bandform,
    })

def addShow(request):
    check(request)
    if request.method == "POST":
        bandform = BandForm(request.POST, request.FILES)
        if bandform.is_valid:
            bandform.save()
            
            #maybe change to the bands new page?
            return redirect("superuser")
    else:
        bandform = BandForm()
    return render(request, "superuser/addband.html",{
        "form": bandform,
    })
    