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
    return HttpResponse("Editor home")


@login_required
def resume(request):
    """
    Add/ edit resumes
    :param request:
    :return:
    """
    if request.method == 'POST':

        # Create a bound form
        form = ResumeForm(request.POST)

        # Return error if same name
        if Resume.objects.filter(name=request.POST.get('name'), user=request.user).count() > 0:
            messages.error(request, "Please chose a different name")
            return HttpResponseRedirect(reverse('resume'))


        # If form is valid, save it.
        if form.is_valid():

            # Save form
            form.instance.user = request.user
            form.save()

            # Add message
            messages.success(request, "New resume {} created".format(form.cleaned_data['name']))

            # Redirect to 'personal' page
            return HttpResponseRedirect(reverse('personal', args=[form.instance.id]))

        # If form is invalid, show errors to user and render form again
        else:
            print str(form.errors.as_data())
            messages.error(request, "Form has errors")
            #return HttpResponseRedirect(reverse('resume'))

            # Handle GET request
            resumes = Resume.objects.filter(user=request.user)

            return render(request, 'builder/resume.html', {'resumes': resumes,
                                                           'form': form})

    # Handle GET request
    resumes = Resume.objects.filter(user=request.user)

    # Display blank form
    form = ResumeForm()
    return render(request, 'builder/resume.html', {'resumes': resumes,
                                                   'form': form})


@login_required
def personal(request, resume_id):
    """
    Handle personal details form
    """

    if request.method == 'POST':

        # Create a bound form using user data
        form = PersonalForm(request.POST)

        if form.is_valid():

            # Get the resume instance
            resume_inst = Resume.objects.get(id=resume_id)

            form.instance.resume = resume_inst
            form.save()

            messages.success(request, "Your personal details are saved")
            return HttpResponseRedirect(reverse('summary', kwargs={'resume_id': resume_id}))
        else:

            # Form is not valid
            print form.errors.as_data()
            messages.error(request, str("Form has errors"))
            return render(request, 'builder/personal.html', {'form': form,
                                                             'resume_id': resume_id})

    try:
        old_data = Personal.objects.get(resume=resume_id)
    except:
        old_data = None

    if old_data is None:
        # New form. Initialize with social account data
        s_user = User.objects.get(id=request.user.id)

        personal_form = PersonalForm(initial={'name': "{} {}".format(s_user.first_name, s_user.last_name),
                                              'email': s_user.email})
    else:
        personal_form = PersonalForm(instance=old_data)

    return render(request, 'builder/personal.html', {'form': personal_form,
                                                     'resume_id': resume_id})


def summary(request, resume_id):
    """
    Handle summary details
    """

    if request.method == 'POST':

        # Create a bound form using user data
        form = SummaryForm(request.POST)

        if form.is_valid():

            # Get the resume instance
            resume_inst = Resume.objects.get(id=resume_id)

            form.instance.resume = resume_inst
            form.save()

            messages.success(request, "Your summary details are saved")
            return HttpResponseRedirect(reverse('education', kwargs={'resume_id': resume_id}))
        else:

            # Form is not valid
            print form.errors.as_data()
            messages.error(request, str("Form has errors"))
            return render(request, 'builder/summary.html', {'form': form,
                                                             'resume_id': resume_id})

    try:
        old_data = Summary.objects.get(resume=resume_id)
    except:
        old_data = None

    if old_data is None:
        # New form. Initialize with social account data
        personal_form = SummaryForm()
    else:
        personal_form = SummaryForm(instance=old_data)

    return render(request, 'builder/summary.html', {'form': personal_form,
                                                     'resume_id': resume_id})



@login_required
def education(request, resume_id):
    """
    Allow users to update education details
    """

    if request.method == 'POST':

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
            messages.error(request, "Form has errors")
            return HttpResponseRedirect(reverse('education', kwargs={'resume_id': resume_id}))

    else:

        if len(Education.objects.filter(resume=resume_id)) > 0:
            formset = EducationFormset(queryset=Education.objects.filter(resume=resume_id))
        else:
            formset = EducationFormset_extra1(queryset=Education.objects.filter(resume=resume_id))

        return render(request, 'builder/education.html', {'formset': formset, 'resume_id': resume_id})


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
            messages.error(request, "Form has errors")
            return HttpResponseRedirect(reverse('experience', kwargs={'resume_id': resume_id}))

    else:

        if len(Education.objects.filter(resume=resume_id)) > 0:
            formset = WorkFormset(queryset=Work.objects.filter(resume=resume_id))
        else:
            formset = WorkFormset_extra1(queryset=Work.objects.filter(resume=resume_id))

        return render(request, 'builder/work.html', {'formset': formset, 'resume_id': resume_id})


@login_required
def skills(request, resume_id):
    res = Resume.objects.get(id=resume_id)
    form = SkillsForm(request.POST or None)

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
            messages.error(request, "Form has errors")
            return render(request, 'builder/skills.html', {'form': form, 'resume_id': resume_id})

    try:
        old_data = Skills.objects.get(resume=res)
    except:
        old_data = None
        pass

    if old_data is None:
         # form = SkillsForm()
        pass
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
    user_summary = Summary.objects.get(resume=res)

    user_summary.summary = "\\item  ".join(e for e in user_summary.summary.split("\r\n"))


    for work_inst in work_set:
        work_inst.work_summary = "\\item  ".join(e for e in work_inst.work_summary.split("\r\n"))

    skills = Skills.objects.get(resume=res)

    rendered = render_to_string('themes/standard.html',
                                {
                                    'personal': app_user,
                                    'education': education_set,
                                    'work': work_set,
                                    'skills': skills,
                                    'summary' : user_summary,
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
    """ Delete a given resume_id. redirect to my resumes page"""

    try:
        res = Resume.objects.get(id=resume_id)
        res_name = res.name
        res.delete()
        messages.warning(request, "Resume {} deleted".format(res_name))
    except Exception as e:
        print e
        print "Cannot delete resume id: {}".format(resume_id)

    return HttpResponseRedirect(reverse('resume'))


