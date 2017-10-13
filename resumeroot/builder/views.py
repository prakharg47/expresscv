import subprocess
import os, shutil

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import *


def home(request):
    return HttpResponse("dsf")


@login_required
def resume(request):
    """
    Add/ edit resumes
    :param request:
    :return:
    """
    if request.method == 'POST':
        # Add new resume object
        form = ResumeForm(request.POST)

        if form.is_valid():
            form.cleaned_data['user'] = request.user
            f = form.save(commit=False)
            f.user = request.user
            saved_resume = f.save()

            messages.success(request, "New resume {} created".format(form.cleaned_data['name']))
            return HttpResponseRedirect(reverse('personal', args=[f.id]))

    try:
        resumes = Resume.objects.filter(user=request.user)
    except:
        resumes = []

    form = ResumeForm()
    return render(request, 'builder/resume.html', {'resumes': resumes,
                                                   'form': form})


@login_required
def personal(request, resume_id):
    """
    Display personal details form
    :param resume_id:
    :param request:
    :return:
    """
    if request.method == 'POST':
        # Handle form submission
        form = PersonalForm(request.POST)
        resume_object = Resume.objects.get(id=resume_id)

        if form.is_valid():
            form.cleaned_data['resume'] = resume_id

            p = Personal(resume=resume_object,
                         name=form.cleaned_data.get("name"),
                         email=form.cleaned_data.get("email"),
                         mobile=form.cleaned_data.get("mobile"),
                         summary=form.cleaned_data.get("summary"),
                         city=form.cleaned_data.get("city"),
                         country=form.cleaned_data.get("country"), )

            p.save()

            # f = form.save(commit=False)
            # f.resume_id = resume_id
            # f.save()

            messages.success(request, "Your personal details are saved")
            return HttpResponseRedirect(reverse('education', kwargs={'resume_id': resume_id}))

    try:
        old_data = Personal.objects.get(resume=resume_id)
    except:
        old_data = None
        pass

    if old_data is None:
        # New form. Initialize with social account data
        s_user = User.objects.get(id=request.user.id)

        personal_form = PersonalForm(initial={'name': "{} {}".format(s_user.first_name, s_user.last_name),
                                              'email': s_user.email})
    else:
        personal_form = PersonalForm(instance=old_data)

    return render(request, 'builder/personal.html', {'form': personal_form,
                                                     'resume_id': resume_id})


@login_required
def experience(request, resume_id):
    """
    Add experience details
    :param resume_id:
    :param request:
    :return:
    """

    if request.method == 'POST':
        # HACK - add arbitrary ids in the request if form.id is null.
        # This is because of bug in dynamic-formset-js
        formset = WorkFormset(request.POST)
        resume_object = Resume.objects.get(id=resume_id)

        if formset.is_valid():

            new_education_objects = []
            for form_dict in formset.cleaned_data:
                new_education_objects.append(Work(resume=resume_object,
                                                  company=form_dict.get('company'),
                                                  designation=form_dict.get('designation'),
                                                  work_summary=form_dict.get('work_summary'),
                                                  city=form_dict.get('city'),
                                                  country=form_dict.get('country'),
                                                  to_year=form_dict.get('to_year'),
                                                  from_year=form_dict.get('from_year')))

            # delete old instances of the user
            Work.objects.filter(resume=resume_id).delete()

            # save new instances
            Work.objects.bulk_create(new_education_objects)

            # Return
            messages.success(request, "Your experience details are saved")
            return HttpResponseRedirect(reverse('skills', kwargs={'resume_id': resume_id}))

        else:
            print "Form is invalid"
            messages.error(request, str(formset.errors))
            return HttpResponseRedirect(reverse('experience', kwargs={'resume_id': resume_id}))

    else:
        formset = WorkFormset(queryset=Work.objects.filter(resume=resume_id))
        return render(request, 'builder/work.html', {'formset': formset,
                                                     'resume_id': resume_id})


@login_required
def education(request, resume_id):
    """
    Allow users to update education details
    :param resume_id:
    :param request:
    :return:
    """
    if request.method == 'POST':

        # HACK - add arbitrary ids in the request if form.id is null.
        # This is because of bug in dynamic-formset-js

        formset = EducationFormset(request.POST)
        resume_object = Resume.objects.get(id=resume_id)

        if formset.is_valid():

            new_education_objects = []
            for form_dict in formset.cleaned_data:
                new_education_objects.append(Education(resume=resume_object,
                                                       college=form_dict.get('college'),
                                                       degree=form_dict.get('degree'),
                                                       major=form_dict.get('major'),
                                                       gpa=form_dict.get('gpa'),
                                                       city=form_dict.get('city'),
                                                       country=form_dict.get('country'),
                                                       to_year=form_dict.get('to_year'),
                                                       from_year=form_dict.get('from_year')))

            # delete old instances of the user
            Education.objects.filter(resume=resume_id).delete()

            # save new instances
            Education.objects.bulk_create(new_education_objects)

            # Return
            messages.success(request, "Your education details are saved")
            return HttpResponseRedirect(reverse('experience', kwargs={'resume_id': resume_id}))

        else:
            print "Form is invalid"
            messages.error(request, str(formset.errors))
            return HttpResponseRedirect(reverse('education', kwargs={'resume_id': resume_id}))

    else:

        if len(Education.objects.filter(resume=resume_id)) > 0:
            formset = EducationFormset(queryset=Education.objects.filter(resume=resume_id))
        else:
            formset = EducationFormset_extra1(queryset=Education.objects.filter(resume=resume_id))

        return render(request, 'builder/education.html', {'formset': formset, 'resume_id': resume_id})


@login_required
def skills(request, resume_id):
    res = Resume.objects.get(id=resume_id)

    if request.method == 'POST':
        # Handle form submission
        form = SkillsForm(request.POST)

        if form.is_valid():
            form.cleaned_data['resume'] = res

            f = form.save(commit=False)
            f.resume_id = resume_id
            f.save()

            # return render(request, 'builder/personal.html')
            messages.success(request, "Your details are saved")
            return HttpResponseRedirect(reverse('skills', kwargs={'resume_id': resume_id}))
        else:
            print form.errors
            return HttpResponseRedirect(reverse('skills', kwargs={'resume_id': resume_id}))

    try:
        old_data = Skills.objects.get(resume=res)
    except:
        old_data = None
        pass

    if old_data is None:
        form = SkillsForm()
    else:
        form = SkillsForm(instance=old_data)

    return render(request, 'builder/skills.html', {'form': form, 'resume_id': resume_id})


@login_required
def publish(request, resume_id):
    res = Resume.objects.get(id=resume_id)

    try:
        app_user = Personal.objects.get(resume=res)
    except Exception as e:
        print e
        raise Http404('Please fill in Personal details first')

    education_set = Education.objects.filter(resume=res)
    work_set = Work.objects.filter(resume=res)
    skills = Skills.objects.get(resume=res)

    rendered = render_to_string('themes/standard.html',
                                {
                                    'personal': app_user,
                                    'education': education_set,
                                    'work': work_set,
                                    'skills': skills,
                                })
    with open('output.tex', 'w') as f:
        f.write(rendered)

    p = subprocess.Popen(["pdflatex", "-interaction=scrollmode", "output.tex"])
    p.communicate()

    # Rename output.pdf to @resume_name.pdf
    resume_name = "{}.pdf".format(res.name)
    shutil.copy('output.pdf', resume_name)

    # send back response
    with open(resume_name , 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename={}'.format(resume_name)
        return response
    pass


def delete_resume(request, resume_id):
    """delete a given resume_id. redirect to my resumes page"""

    try:
        r = Resume.objects.get(id=resume_id)
        r.delete()

    except:
        pass

    return HttpResponseRedirect(reverse('resume'))
