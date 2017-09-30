import os
import subprocess

from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.forms.formsets import formset_factory
from django.shortcuts import render, render_to_response
from django.http import *
from django.contrib.auth.models import User

from django.template.loader import render_to_string
from django.urls import reverse

from .models import *
from .forms import *
from django.contrib import messages


# Create your views here.


def home(request):
    return HttpResponse("dsf")


def personal(request):
    """
    Display personal details form
    :param request:
    :return:
    """

    user_id = request.user.id

    if request.method == 'POST':
        # Handle form submission
        form = PersonalForm(request.POST)

        if form.is_valid():

            form.cleaned_data['user'] = request.user
            f = form.save(commit=False)
            f.user = request.user
            f.save()

            # return render(request, 'builder/personal.html')
            return HttpResponseRedirect(reverse('personal'))

    try:
        old_data = Personal.objects.get(user=request.user)
    except :
        old_data = None
        pass

    if old_data is None:
        personal_form = PersonalForm()
    else:
        personal_form = PersonalForm(instance=old_data)

    return render(request, 'builder/personal.html', {'form': personal_form})


def experience(request):
    if request.method == 'POST':
        # Handle POST form data

        form = WorkFormset(request.POST)
        instances = form.save(commit=False)

        for instance in instances:
            instance.user = request.user
            instance.save()

        return HttpResponseRedirect(reverse('experience'))

    # Render fresh form
    form = WorkFormset(queryset=Work.objects.filter(user=request.user))
    return render(request, 'builder/work.html', {'formset': form})


def education(request):
    """
    Allow users to update education details
    :param request:
    :return:
    """
    if request.method == 'POST':

        # HACK - add arbitrary ids in the request if form.id is null.
        # This is because of bug in dynamic-formset-js

        formset = EducationFormset(request.POST)



        print formset
        print "-----"
        if formset.is_valid():
            # Delete older user data. Save new form data
            print formset.cleaned_data
            print Education.objects.filter(user=request.user)

            new_education_objects = []
            for form_dict in formset.cleaned_data:
                new_education_objects.append(Education(user=request.user, college=form_dict.get('college')))

            # delete old instances of the user
            Education.objects.filter(user=request.user).delete()

            # save new instances
            Education.objects.bulk_create(new_education_objects)

            # # Save new instances
            # instances = formset.save(commit=False)
            # print "\n\n printing instances ...."
            # print instances
            #
            # for instance in instances:
            #     print "\n\n printing instance ----- ...."
            #     print instance.id
            #     instance.user = request.user
            #     instance.save()

            # Return
            messages.success(request, "Your education details are saved")
            return HttpResponseRedirect(reverse('education'))

        else:
            print "Form is invalid"
            messages.error(request, str(formset.errors))
            return HttpResponseRedirect(reverse('education'))

    else:
        formset = EducationFormset(queryset=Education.objects.filter(user=request.user))
        return render(request, 'builder/education.html', {'formset': formset})


def education2(request):

    if request.method == 'POST':
        # Handle POST form data

        form = EducationFormset(request.POST)
        print "---------------"
        for f in form:
            print f
            print " *********"
            print " "
        print "---------------"

        if form.is_valid():

            instances = form.save(commit=False)
            # Delete older entries
            #Education.objects.filter(user=request.user).delete()

            print "Printing instances ... "
            for instance in instances:
                print instance
                instance.user = request.user
                instance.save()

        return HttpResponseRedirect(reverse('education'))

    # Render fresh form
    form = EducationFormset(queryset=Education.objects.filter(user=request.user))
    return render(request, 'builder/education.html', {'formset': form})


def publish(request):

    current_user = request.user
    print request.user

    try:
        app_user = Personal.objects.get(user=request.user.id)
    except:
        print "app user doesnt exist"
        raise Http404('User doesnt exist. Please fill in details for that user first')

    education_set = Education.objects.filter(user=request.user)
    work_set = Work.objects.filter(user=request.user)

    rendered = render_to_string('themes/standard.html',
                                {
                                    'personal': app_user,
                                    'education' : education_set,
                                    'work' : work_set
                                 })
    with open('output.tex', 'w') as f:
        f.write(rendered)

    p = subprocess.Popen(["pdflatex", "-interaction=scrollmode", "output.tex"])
    p.communicate()

    with open('output.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        #response['Content-Disposition'] = 'inline;filename=test.pdf'
        return response
    pass

