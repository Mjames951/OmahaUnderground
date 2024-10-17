from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *
import datetime




# Create your views here.
def index(request):
    context = None
    return render(request, 'planetplum/index.html', context=context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index') #change to login

        return redirect("index")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})