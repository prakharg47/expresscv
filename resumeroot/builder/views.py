import subprocess

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import *


# Create your views here.


def home(request):
    return HttpResponse("dsf")


@login_required
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
            messages.success(request, "Your personal details are saved")
            return HttpResponseRedirect(reverse('personal'))

    try:
        old_data = Personal.objects.get(user=request.user)
    except:
        old_data = None
        pass

    if old_data is None:
        personal_form = PersonalForm()
    else:
        personal_form = PersonalForm(instance=old_data)

    return render(request, 'builder/personal.html', {'form': personal_form})


@login_required
def experience(request):
    """
    Add experience details
    :param request:
    :return:
    """

    if request.method == 'POST':

        # HACK - add arbitrary ids in the request if form.id is null.
        # This is because of bug in dynamic-formset-js

        formset = WorkFormset(request.POST)

        if formset.is_valid():
            # Delete older user data. Save new form data
            print formset.cleaned_data
            print Work.objects.filter(user=request.user)

            new_education_objects = []
            for form_dict in formset.cleaned_data:
                new_education_objects.append(Work(user=request.user,
                                                       company=form_dict.get('company'),
                                                       designation=form_dict.get('designation'),
                                                       work_summary=form_dict.get('work_summary'),
                                                       city=form_dict.get('city'),
                                                       country=form_dict.get('country'),
                                                       to_year=form_dict.get('to_year'),
                                                       from_year=form_dict.get('from_year')))

            # delete old instances of the user
            Work.objects.filter(user=request.user).delete()

            # save new instances
            Work.objects.bulk_create(new_education_objects)

            # Return
            messages.success(request, "Your experience details are saved")
            return HttpResponseRedirect(reverse('experience'))

        else:
            print "Form is invalid"
            messages.error(request, str(formset.errors))
            return HttpResponseRedirect(reverse('experience'))

    else:
        formset = WorkFormset(queryset=Work.objects.filter(user=request.user))
        return render(request, 'builder/work.html', {'formset': formset})


@login_required
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

        if formset.is_valid():
            # Delete older user data. Save new form data
            print formset.cleaned_data
            print Education.objects.filter(user=request.user)

            new_education_objects = []
            for form_dict in formset.cleaned_data:
                new_education_objects.append(Education(user=request.user,
                                                       college=form_dict.get('college'),
                                                       degree=form_dict.get('degree'),
                                                       major=form_dict.get('major'),
                                                       gpa=form_dict.get('gpa'),
                                                       city=form_dict.get('city'),
                                                       country=form_dict.get('country'),
                                                       to_year=form_dict.get('to_year'),
                                                       from_year=form_dict.get('from_year')))

            # delete old instances of the user
            Education.objects.filter(user=request.user).delete()

            # save new instances
            Education.objects.bulk_create(new_education_objects)

            # Return
            messages.success(request, "Your education details are saved")
            return HttpResponseRedirect(reverse('education'))

        else:
            print "Form is invalid"
            messages.error(request, str(formset.errors))
            return HttpResponseRedirect(reverse('education'))

    else:

        if len(Education.objects.filter(user=request.user)) > 0:
            formset = EducationFormset(queryset=Education.objects.filter(user=request.user))
        else:
            formset = EducationFormset_extra1(queryset=Education.objects.filter(user=request.user))

        return render(request, 'builder/education.html', {'formset': formset})


@login_required
def publish(request):
    current_user = request.user
    print request.user

    try:
        app_user = Personal.objects.get(user=request.user.id)
        print app_user.summary + "************"
    except:
        print "app user doesnt exist"
        raise Http404('User doesnt exist. Please fill in details for that user first')

    education_set = Education.objects.filter(user=request.user)
    work_set = Work.objects.filter(user=request.user)

    rendered = render_to_string('themes/standard.html',
                                {
                                    'personal': app_user,
                                    'education': education_set,
                                    'work': work_set
                                })
    with open('output.tex', 'w') as f:
        f.write(rendered)

    p = subprocess.Popen(["pdflatex", "-interaction=scrollmode", "output.tex"])
    p.communicate()

    with open('output.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        # response['Content-Disposition'] = 'inline;filename=test.pdf'
        return response
    pass


def skills(request):
    user_id = request.user.id

    if request.method == 'POST':
        # Handle form submission
        form = SkillsForm(request.POST)

        if form.is_valid():
            form.cleaned_data['user'] = request.user
            f = form.save(commit=False)
            f.user = request.user
            f.save()

            # return render(request, 'builder/personal.html')
            messages.success(request, "Your personal details are saved")
            return HttpResponseRedirect(reverse('personal'))

    try:
        old_data = Skills.objects.get(user=request.user)
    except:
        old_data = None
        pass

    if old_data is None:
        form = SkillsForm()
    else:
        form = SkillsForm(instance=old_data)

    return render(request, 'builder/skills.html', {'form': form})


