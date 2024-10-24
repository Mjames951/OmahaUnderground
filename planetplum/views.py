from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *
import datetime




# Create your views here.
def index(request):
    context = None
    return render(request, 'planetplum/index.html', context=context)

def about(request):
    return render(request, 'planetplum/about.html', context=None)

def feedback(request):
    submitted = False
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            user = request.user
            username = user.username
            email = user.email
            content = form.cleaned_data['content']

            # replace this with an email handler to email me the response
            print(f"{username} at {email} says: {content}")

            form = FeedbackForm()
            submitted = True
    else:
        form = FeedbackForm()
    return render(request, "planetplum/feedback.html", {
                      "form": form,
                      "submitted": submitted,
                      })

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') #change to login

        return redirect("index")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})