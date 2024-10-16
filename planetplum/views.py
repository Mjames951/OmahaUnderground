from django.shortcuts import render, get_object_or_404, redirect

from .models import *
import datetime




# Create your views here.
def index(request):
    context = None
    return render(request, 'planetplum/index.html', context=context)