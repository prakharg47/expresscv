from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import *

# Create your views here.


def home(request):
    return HttpResponse("you are logged in")
