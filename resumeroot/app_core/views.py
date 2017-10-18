from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.


def home(request):

    total_users = len(User.objects.all())

    return render(request, 'app_core/home.html', context={'total_users': total_users})


def pricing(request):

    return render (request, 'app_core/pricing.html', {})