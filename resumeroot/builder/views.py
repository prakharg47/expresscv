from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import *
from django.contrib.auth.models import User

from builder.forms import EducationFormSetHelper
from . import models
from . import forms
# Create your views here.


def home(request):
    # print User.objects.all()
    # print request.user

    if request.method == 'POST':
        with open('/tmp/test.pdf', 'r') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=test.pdf'
            return response

    form = forms.ResumeForm()
    education_formset = forms.EducationFormSet()
    helper2 = EducationFormSetHelper()

    return render(request, 'builder/home.html', {'form': form, 'ed_formset': education_formset, 'helper2': helper2})


