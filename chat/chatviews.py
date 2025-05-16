from django.shortcuts import render, get_object_or_404, redirect
from .chatforms import ChannelPostForm
from .models import  Channel, ChannelSection, Post, Report
from django.conf import settings
from planetplum.tools.imagehandler import addImage

def chat(request):
    channelsections = ChannelSection.objects.all().reverse()
    return render(request, "chat/chat.html", {
        "sections" : channelsections
    })


chatload = settings.CHAT_LOAD

def channel(request, channelname, load):
    user = request.user
    try:  channel = get_object_or_404(Channel, name=channelname)
    except: return redirect("chat")
    if request.method == "POST":
        if not user.is_authenticated:
            return redirect('login')
        form = ChannelPostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            if form.cleaned_data['text'] == "" and form.cleaned_data['image'] == None:
                return redirect("channel", channelname, load)

            post = form.save(commit=False)
            post.user = user
            post.channel = channel

            #image resizing
            addImage(form, 'show')

            post.save()
            form = ChannelPostForm()
            return redirect("channel", channelname, load)

    else: form = ChannelPostForm()

    posts = channel.post_set.all().order_by('-timestamp')[:chatload*load]
    posts = reversed(posts)
    return render(request, "chat/channel.html", {
        "form": form,
        "posts": posts,
        "load": load+1,
        "channel": channel.name,
    })

def report(request, channelname, load, postid):
    try: 
        post = get_object_or_404(Post, id=postid)
        channel = get_object_or_404(Channel, name=channelname)
    except: return redirect("chat")
    if not Report.objects.filter(post=post):
        newReport = Report(post=post, channel=channel)
        newReport.save()
    return render(request, "chat/reportsuccess.html", None)

def delete(request, channelname, load, postid):
    try: 
        post = get_object_or_404(Post, id=postid)
    except: return redirect("chat")
    if post.user != request.user:
        return redirect("chat")
    try: post.delete()
    except: return redirect("index")
    return redirect("channel", str(channelname), int(load))
