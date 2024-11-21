from django.shortcuts import render, get_object_or_404, redirect
from .chatforms import ChannelPostForm
from .models import channel as Channel
from .models import channelSection

def chat(request):
    channelsections = channelSection.objects.all()
    return render(request, "chat/chat.html", {
        "sections" : channelsections
    })

def channel(request, channel):
    user = request.user
    try:  channel = get_object_or_404(Channel, name=channel)
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
            return redirect('channel', channel.name)
        #give the user an error and handle image sent

    form = ChannelPostForm()

    posts = channel.post_set.all()
    posts = posts.order_by('timestamp')
    return render(request, "chat/channel.html", {
        "form": form,
        "posts": posts,
    })