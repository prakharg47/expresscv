import shutil
import subprocess
from wsgiref.util import FileWrapper

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.http import Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from builder.forms import *
from builder.views import html_to_latex

import publish.utils as utils

@login_required
def publish(request, resume_id):
    themes = [
        (0, 'standard'),
        (1, 'express'),
        (2, 'compact'),
        (3, 'modern')
    ]

    res = Resume.objects.get(id=resume_id)
    theme = Theme.objects.get(resume_id=resume_id)

    try:
        app_user = Personal.objects.get(resume=res)
    except Exception as e:
        raise Http404('Please fill in Personal details first')

    app_user.email = utils.unescape_email(app_user.email)

    education_set = Education.objects.filter(resume=res)
    for work_inst in education_set:
        # work_inst.work_summary = "\\item  ".join(e for e in work_inst.work_summary.split("\r\n"))
        work_inst.education_summary = html_to_latex(work_inst.education_summary).replace("\n", " ").replace("\r", "")

    try:
        user_summary = Summary.objects.get(resume=res)
        user_summary.summary = html_to_latex(user_summary.summary)
    except Summary.DoesNotExist:
        user_summary = None

    work_set = Work.objects.filter(resume=res)
    for work_inst in work_set:
        # work_inst.work_summary = "\\item  ".join(e for e in work_inst.work_summary.split("\r\n"))
        work_inst.work_summary = html_to_latex(work_inst.work_summary).replace("\n", " ").replace("\r", "")

    try:
        skills = Skills.objects.get(resume=res)
    except Skills.DoesNotExist:
        skills = None

    skills.skills = html_to_latex(skills.skills).replace("\n", " ").replace("\r", "\n")
    print ("Skills are {}".format(skills))

    try:
        language = Languages.objects.get(resume=res)
    except Languages.DoesNotExist:
        language = None

    language.languages = html_to_latex(language.languages).replace("\n", " ").replace("\r", "\n")

    print("Languages are {}".format(language))

    # language.languages = html_to_latex(language.languages)

    try:
        theme_detail = Theme.objects.get(resume=res)
    except Exception:
        theme_detail = None

    award_set = Award.objects.filter(resume=res)
    for a in award_set:
        a.award_summary = html_to_latex(a.award_summary).replace("\n", " ").replace("\r", "")

    ttt = theme_detail.theme

    # rendered = render_to_string('old_themes/{}.html'.format(ttt),
    rendered = render_to_string('themes/{}.html'.format("mahrez"),
                                {
                                    'theme_details': theme_detail,
                                    'personal': app_user,
                                    'educations': education_set,
                                    'works': work_set,
                                    'skills': skills,
                                    'summary': user_summary,
                                    'languages': language,
                                    'awards' : award_set
                                })
    with open('output.tex', 'w') as f:
        f.write(rendered)

    p = subprocess.Popen(["xelatex", "-interaction=scrollmode", "output.tex"])
    p.communicate()

    # Rename output.pdf to @resume_name.pdf
    resume_name = "{}.pdf".format(res.name)
    shutil.copy('output.pdf', resume_name)

    # send back response
    # with open(resume_name, 'r') as pdf:
    # response = HttpResponse(pdf.read(), content_type='application/pdf')
    response = HttpResponse(FileWrapper(open(resume_name, 'rb')), content_type='application/pdf')
    response['Content-Disposition'] = 'inline;filename={}'.format(resume_name)
    return response


def preview(request, resume_id):
    """previews a inline pdf. Also allows further fine tuning """

    # generate the pdf ('output.pdf')
    # publish(request, resume_id)
    if request.method == 'POST':

        # Create a bound form using user data
        form = ThemesModelForm(request.POST)

        # font = request.POST.get('font_family')
        # theme = request.POST.get('theme')
        #
        # form.fields['font_family'] = [(font, font)]
        # form.fields['theme'] = [(theme, theme)]

        if form.is_valid():

            # Get the resume instance
            resume_inst = Resume.objects.get(id=resume_id)

            form.instance.resume = resume_inst
            form.save()

            messages.success(request, "Your summary details are saved")
            return HttpResponseRedirect(reverse('preview', kwargs={'resume_id': resume_id}))
        else:

            # Form is not valid

            messages.error(request, str("Form has errors"))
            return render(request, 'builder/preview.html', {'form': form,
                                                            'resume_id': resume_id})

    try:
        old_data = Theme.objects.get(resume=resume_id)
    except:
        old_data = None

    if old_data is None:
        # New form. Initialize with social account data
        personal_form = ThemesModelForm()
    else:
        personal_form = ThemesModelForm(instance=old_data)

    return render(request, 'builder/preview.html', {'pdf': 'output.pdf', 'resume_id': resume_id,
                                                    'form': personal_form})
