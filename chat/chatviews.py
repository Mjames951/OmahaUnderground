from django.shortcuts import render, get_object_or_404, redirect
from .chatforms import ChannelPostForm
from .models import channel as Channel
from .models import channelSection
from django.conf import settings

def chat(request):
    channelsections = channelSection.objects.all()
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
            post = form.save(commit=False)
            post.user = user
            post.channel = channel
            post.save()
            return redirect('channel', channelname, load)
        #give the user an error and handle image sent

    form = ChannelPostForm()

    posts = channel.post_set.all().order_by('-timestamp')[chatload*load-chatload:chatload*load]
    posts = reversed(posts)
    return render(request, "chat/channel.html", {
        "form": form,
        "posts": posts,
        "load": load+1,
        "channel": channel.name,
    })