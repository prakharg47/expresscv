import shutil
import subprocess
from wsgiref.util import FileWrapper

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import *

# Global defaults
FORM_ERROR_MESSAGE = "Form has errors. Please fill the form again"


@login_required
def resume(request):
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

            default_theme = Theme(resume_id=form.instance.id)
            default_theme.save()

            # Add message
            messages.success(request, "New resume {} created".format(form.cleaned_data['name']))

            # Redirect to 'choose theme' page
            return HttpResponseRedirect(reverse('theme', args=[form.instance.id]))

        # If form is invalid, show errors to user and render form again
        else:
            messages.error(request, FORM_ERROR_MESSAGE)

            # Handle GET request
            resumes = Resume.objects.filter(user=request.user)

            return render(request, 'builder/resume.html', {'resumes': resumes, 'form': form})

    # Handle GET request
    resumes = Resume.objects.filter(user=request.user)

    # Display blank form
    form = ResumeForm()
    return render(request, 'builder/resume.html', {'resumes': resumes,
                                                   'form': form})


@login_required
def theme(request, resume_id):
    """
    Choose theme for a resume
    """
    res = Resume.objects.get(id=resume_id)
    # form = SkillsForm(request.POST)

    if request.method == 'POST':
        # Handle form submission
        form = ThemesChoiceForm(request.POST)

        if form.is_valid():

            new_theme = Theme()
            new_theme.theme = form.cleaned_data['theme_name']
            new_theme.resume_id = resume_id
            new_theme.save()

            messages.success(request, "Theme is saved")

            return HttpResponseRedirect(reverse('personal', kwargs={'resume_id': resume_id}))
        else:
            messages.error(request, "Form has errors")
            return render(request, 'builder/theme.html', {'form': form, 'resume_id': resume_id})

    form = ThemesChoiceForm()

    return render(request, 'builder/theme.html', {'form': form, 'resume_id': resume_id})


class PersonalView(FormView):
    template_name = 'builder/personal.html'
    form_class = PersonalForm
    success_url = '/education/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(self).form_valid(form)


@login_required
def personal(request, resume_id):
    if request.method == 'POST':

        # Create a bound form using user data
        form = PersonalForm(request.POST, request.FILES)

        if form.is_valid():

            # Get the resume instance
            resume_inst = Resume.objects.get(id=resume_id)

            form.instance.resume = resume_inst
            form.save()

            messages.success(request, "Your personal details are saved")
            return HttpResponseRedirect(reverse('summary', kwargs={'resume_id': resume_id}))
        else:

            # Form is not valid
            messages.error(request, str("Form has errors"))
            return render(request, 'builder/personal.html', {'form': form,
                                                             'resume_id': resume_id})

    try:
        old_data = Personal.objects.get(resume=resume_id)
    except Exception as e:
        print(e)
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

            messages.error(request, "Form has errors")
            return HttpResponseRedirect(reverse('experience', kwargs={'resume_id': resume_id}))

    else:

        if len(Work.objects.filter(resume=resume_id)) > 0:
            formset = WorkFormset(queryset=Work.objects.filter(resume=resume_id))
        else:
            formset = WorkFormset_extra1(queryset=Work.objects.filter(resume=resume_id))

        return render(request, 'builder/work.html', {'formset': formset, 'resume_id': resume_id})


@login_required
def skills(request, resume_id):
    res = Resume.objects.get(id=resume_id)
    # form = SkillsForm(request.POST or None)

    form = SkillsForm(request.POST)

    if request.method == 'POST':
        # Handle form submission
        form = SkillsForm(request.POST)

        if form.is_valid():
            form.instance.resume = res
            form.save()

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


def languages(request, resume_id):
    res = Resume.objects.get(id=resume_id)
    # form = SkillsForm(request.POST or None)

    form = LanguagesForm(request.POST)

    if request.method == 'POST':
        # Handle form submission
        form = LanguagesForm(request.POST)

        if form.is_valid():

            form.instance.resume = res
            form.save()

            messages.success(request, "Your details are saved")
            return HttpResponseRedirect(reverse('languages', kwargs={'resume_id': resume_id}))
        else:
            messages.error(request, "Form has errors")
            return render(request, 'builder/languages.html', {'form': form, 'resume_id': resume_id})

    try:
        old_data = Languages.objects.get(resume=res)
    except:
        old_data = None
        pass

    if old_data is None:
        # form = SkillsForm()
        pass
    else:
        form = LanguagesForm(instance=old_data)

    return render(request, 'builder/languages.html', {'form': form, 'resume_id': resume_id})


def html_to_latex(html):
    html = html.replace("<ol>", "\\begin{enumerate} ")
    html = html.replace("</ol>", "\\end{enumerate} ")
    html = html.replace("<ul>", "\\begin{itemize} ")
    html = html.replace("</ul>", "\\end{itemize} ")

    html = html.replace("<li>", "\\item ")
    html = html.replace("</li>", " ")
    html = html.replace("<p>", " ")
    html = html.replace("</p>", " ")

    html = html.replace("<strong>", "\\textbf{")
    html = html.replace("</strong>", "} ")
    html = html.replace("<em>", "\\textit{")
    html = html.replace("</em>", "} ")
    html = html.replace("<u>", "\\underline{")
    html = html.replace("</u>", "} ")

    html = html.replace("&nbsp;", " ")

    return html



def delete_resume(request, resume_id):
    """ Delete a given resume_id. redirect to my resumes page"""

    try:
        res = Resume.objects.get(id=resume_id)
        res_name = res.name
        res.delete()
        messages.warning(request, "Resume {} deleted".format(res_name))
    except Exception as e:
        pass

    return HttpResponseRedirect(reverse('resume'))


@login_required
def experience_all(request, resume_id):
    res = Resume.objects.get(id=resume_id)
    work_objects = Work.objects.filter(resume=resume_id)

    return render(request, 'builder/experience_all.html', {'work_objects': work_objects,
                                                           'resume_id': resume_id})


def experience_new(request, resume_id):
    res = Resume.objects.get(id=resume_id)

    if request.method == 'POST':
        # handle new work form

        form = ExperienceForm(request.POST)

        if form.is_valid():
            form.instance.resume = res
            form.save()

            messages.success(request, "Your details are saved")
            return HttpResponseRedirect(reverse('experience', kwargs={'resume_id': resume_id}))
        else:
            messages.error(request, "Form has errors")
            return render(request, 'builder/experience_new.html', {'form': form, 'resume_id': resume_id})

    form = ExperienceForm()

    return render(request, 'builder/experience_new.html', {'form': form,
                                                           'resume_id': resume_id})


def experience_edit(request, resume_id, work_id):
    res = Resume.objects.get(id=resume_id)
    old_work_object = Work.objects.get(resume=res, id=work_id)

    if request.method == 'POST':
        # handle new work form

        form = ExperienceForm(request.POST, instance=old_work_object)

        if form.is_valid():
            form.instance.resume = res
            form.save()

            messages.success(request, "Your details are saved")
            return HttpResponseRedirect(reverse('experience', kwargs={'resume_id': resume_id}))
        else:
            messages.error(request, "Form has errors")
            return render(request, 'builder/experience_new.html', {'form': form, 'resume_id': resume_id})

    old_work_object = Work.objects.get(resume=res, id=work_id)

    form = ExperienceForm(instance=old_work_object)

    return render(request, 'builder/experience_edit.html', {'form': form,
                                                            'resume_id': resume_id, 'work_id': work_id})


def experience_delete(request, resume_id, work_id):
    """ Delete a given resume_id. redirect to my resumes page"""

    try:
        res = Resume.objects.get(id=resume_id)
        res_name = res.name
        work_object = Work.objects.get(resume=res, id=work_id)
        work_object.delete()
        messages.warning(request, "Experience {} deleted".format(res_name))
    except Exception as e:
        pass

    return HttpResponseRedirect(reverse('experience', kwargs={'resume_id': resume_id}))


@login_required
def education_all(request, resume_id):
    res = Resume.objects.get(id=resume_id)
    work_objects = Education.objects.filter(resume=resume_id)

    return render(request, 'builder/education_all.html', {'work_objects': work_objects,
                                                          'resume_id': resume_id})


@login_required
def education_new(request, resume_id):
    res = Resume.objects.get(id=resume_id)

    if request.method == 'POST':
        # handle new work form

        form = EducationNewForm(request.POST)

        if form.is_valid():
            form.instance.resume = res
            form.save()

            messages.success(request, "Your details are saved")
            return HttpResponseRedirect(reverse('education', kwargs={'resume_id': resume_id}))
        else:
            messages.error(request, "Form has errors")
            return render(request, 'builder/education_new.html', {'form': form, 'resume_id': resume_id})

    form = EducationNewForm()

    return render(request, 'builder/education_new.html', {'form': form,
                                                          'resume_id': resume_id})


@login_required
def education_edit(request, resume_id, ed_id):
    res = Resume.objects.get(id=resume_id)
    old_work_object = Education.objects.get(resume=res, id=ed_id)

    if request.method == 'POST':
        # handle new work form

        form = EducationNewForm(request.POST, instance=old_work_object)

        if form.is_valid():
            form.instance.resume = res
            form.save()

            messages.success(request, "Your details are saved")
            return HttpResponseRedirect(reverse('education', kwargs={'resume_id': resume_id}))
        else:
            messages.error(request, "Form has errors")
            return render(request, 'builder/education_edit.html', {'form': form, 'resume_id': resume_id})

    old_work_object = Education.objects.get(resume=res, id=ed_id)

    form = EducationNewForm(instance=old_work_object)

    return render(request, 'builder/education_edit.html', {'form': form,
                                                           'resume_id': resume_id, 'ed_id': ed_id})


@login_required
def education_delete(request, resume_id, ed_id):
    """ Delete a given resume_id. redirect to my resumes page"""

    try:
        res = Resume.objects.get(id=resume_id)
        res_name = res.name
        work_object = Education.objects.get(resume=res, id=ed_id)
        work_object.delete()
        messages.warning(request, "Education {} deleted".format(res_name))
    except Exception as e:
        pass

    return HttpResponseRedirect(reverse('education', kwargs={'resume_id': resume_id}))


# Awards section

@login_required
def award_all(request, resume_id):
    res = Resume.objects.get(id=resume_id)
    work_objects = Award.objects.filter(resume=resume_id)

    return render(request, 'builder/award_all.html', {'work_objects': work_objects,
                                                           'resume_id': resume_id})


def award_new(request, resume_id):
    res = Resume.objects.get(id=resume_id)

    if request.method == 'POST':
        # handle new work form

        form = AwardForm(request.POST)

        if form.is_valid():
            form.instance.resume = res
            form.save()

            messages.success(request, "Your details are saved")
            return HttpResponseRedirect(reverse('award', kwargs={'resume_id': resume_id}))
        else:
            messages.error(request, "Form has errors")
            return render(request, 'builder/award_new.html', {'form': form, 'resume_id': resume_id})

    form = AwardForm()

    return render(request, 'builder/award_new.html', {'form': form,
                                                           'resume_id': resume_id})


def award_edit(request, resume_id, award_id):
    res = Resume.objects.get(id=resume_id)
    old_award_object = Award.objects.get(resume=res, id=award_id)

    if request.method == 'POST':
        # handle new work form

        form = AwardForm(request.POST, instance=old_award_object)

        if form.is_valid():
            form.instance.resume = res
            form.save()

            messages.success(request, "Your details are saved")
            return HttpResponseRedirect(reverse('award', kwargs={'resume_id': resume_id}))
        else:
            messages.error(request, "Form has errors")
            return render(request, 'builder/award_new.html', {'form': form, 'resume_id': resume_id})

    old_award_object = Award.objects.get(resume=res, id=award_id)

    form = AwardForm(instance=old_award_object)

    return render(request, 'builder/award_edit.html', {'form': form,
                                                            'resume_id': resume_id, 'award_id': award_id})


def award_delete(request, resume_id, award_id):
    """ Delete a given resume_id. redirect to my resumes page"""

    try:
        res = Resume.objects.get(id=resume_id)
        res_name = res.name
        work_object = Award.objects.get(resume=res, id=award_id)
        work_object.delete()
        messages.warning(request, "Award {} deleted".format(res_name))
    except Exception as e:
        pass

    return HttpResponseRedirect(reverse('award', kwargs={'resume_id': resume_id}))
