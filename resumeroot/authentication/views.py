from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as djlogout
from django.urls import reverse

# Create your views here.
def logout(request):

    djlogout(request)

    return HttpResponseRedirect(reverse('root_home'))