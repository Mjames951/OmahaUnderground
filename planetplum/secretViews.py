from django.shortcuts import render, get_object_or_404, redirect

from .models import *
import datetime

def index(request):
    context = None
