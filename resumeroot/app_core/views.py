from django.shortcuts import render

# Create your views here.


def home(request):
    print 'requested Home'
    return render(request, 'app_core/home.html', context=None)