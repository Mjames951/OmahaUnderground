from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .chatforms import *
import datetime
from django.views import View

def check(request):
    if not request.user.is_superuser:
        return redirect('index')

def addChannel(request):
    check(request)
    if request.method == 'POST':
        channelform = ChannelForm(request.POST)
        if channelform.is_valid():
            channelform.save()

            return redirect('chat')
    else:
        channelform = ChannelForm()
    return render(request, "superuser/addchannel.html",{
        "form": channelform,
    })

def addChannelSection(request):
    check(request)
    if request.method == "POST":
        form = ChannelSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat')
    else:
        form = ChannelSectionForm()
    return render(request, "superuser/addchannelsection.html", {
        "form": form,
    })