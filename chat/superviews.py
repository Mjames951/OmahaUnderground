from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .chatforms import *
import datetime
from django.views import View
from planetplum.tools.userhandler import ConfirmUser

def chatList(request):
    if not ConfirmUser(request.user): return redirect("index")
    sections = ChannelSection.objects.all()
    return render(request, "superuser/chatlist.html", {
        "sections": sections,
    })

def addChannel(request):
    if not ConfirmUser(request.user): return redirect('index')
    if request.method == 'POST':
        channelform = ChannelForm(request.POST)
        if channelform.is_valid():
            channelform.save()

            return redirect('chat')
    else: channelform = ChannelForm()
    return render(request, "superuser/addchannel.html",{
        "form": channelform,
    })

def editChannel(request, channelid):
    if not ConfirmUser(request.user): return redirect("index")
    channel = get_object_or_404(Channel, id=channelid)
    if request.method == "POST":
        form = ChannelForm(request.POST, instance=channel)
        if form.is_valid():
            form.save()
        return redirect("chat")
    else:
        form = ChannelForm(instance=channel)
    return render(request, "superuser/editchat.html", {
        "form": form,
    })

def addChannelSection(request):
    if not ConfirmUser(request.user): return redirect('index')
    if request.method == "POST":
        form = ChannelSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat')
    else: form = ChannelSectionForm()
    return render(request, "superuser/addchannelsection.html", {
        "form": form,
    })

def editChannelSection(request, sectionid):
    if not ConfirmUser(request.user): return redirect("index")
    section = get_object_or_404(ChannelSection, id=sectionid)
    if request.method == "POST":
        form = ChannelSectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
        return redirect("chat")
    else:
        form = ChannelSectionForm(instance=section)
    return render(request, "superuser/editchat.html", {
        "form": form,
    })