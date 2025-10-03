from django.shortcuts import render, get_object_or_404, redirect
from .chatforms import TopicForm, PostForm
from .models import  Root, Topic, Post, Report
from django.conf import settings
from planetplum.tools.imagehandler import addImage

from django.core.paginator import Paginator

def chat(request):
    roots = Root.objects.all()
    paginator = Paginator(roots, 2)
    pageNumber = request.GET.get("page")
    pageObject = paginator.get_page(pageNumber)
    rootPosts = []

    for root in pageObject:
        rootPosts.append([root, root.replies.all().last])

    return render(request, "chat/chat.html", {
        "pageobj": pageObject,
        'rootposts': rootPosts
    })



chatload = settings.CHAT_LOAD

def root(request, name):
    user = request.user
    root = get_object_or_404(Root, name=name)

    if request.method == "POST":
        if not user.is_authenticated: return redirect('login')
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            if form.cleaned_data['text'] == "" and form.cleaned_data['image'] == None: return redirect("root", rootpostid, load)

            reply = form.save(commit=False)
            reply.user = user
            reply.root = root

            #image resizing
            addImage(form, 'show')

            reply.save()
            form = TopicForm()
            return redirect("root", name)

    else: form = TopicForm()

    replies = root.replies.all().order_by('-timestamp')#[:chatload*load]
    replies = reversed(replies)
    return render(request, "chat/channel.html", {
        "form": form,
        "replies": replies,
        "root": root,
    })

def report(request, channelname, load, postid):
    post = get_object_or_404(Post, id=postid)
    root = get_object_or_404(Root, name=channelname)
    if not Report.objects.filter(post=post):
        newReport = Report(post=post, root=root)
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
    return redirect("root", str(channelname), int(load))
