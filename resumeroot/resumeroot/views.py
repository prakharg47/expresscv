from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import *

# Create your views here.


def home(request):
    print "**********"
    return render(request, 'resumeroot/home.html', context=None)
