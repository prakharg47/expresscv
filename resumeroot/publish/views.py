import shutil
import subprocess
from wsgiref.util import FileWrapper
import re

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

    user_resume = Resume.objects.get(id=resume_id)

    try:
        theme_detail = Theme.objects.get(resume=user_resume)
    except Theme.DoesNotExist:
        raise Http404('Please choose a theme first')

    try:
        app_user = Personal.objects.get(resume=user_resume)
    except Personal.DoesNotExist:
        raise Http404('Please fill in Personal details first')

    # un-escape email according to latex rules
    app_user.email = utils.unescape_email(app_user.email)

    education_set = Education.objects.filter(resume=user_resume)

    for elem in education_set:
        elem.education_summary = convert_html_to_latex(elem.education_summary, theme_detail.theme)\
            .replace("\n", " ")\
            .replace("\r", "")

    try:
        user_summary = Summary.objects.get(resume=user_resume)
        user_summary.summary = convert_html_to_latex(user_summary.summary, theme_detail.theme)
    except Summary.DoesNotExist:
        user_summary = None

    work_set = Work.objects.filter(resume=user_resume)
    for elem in work_set:
        elem.work_summary = convert_html_to_latex(elem.work_summary, theme_detail.theme)\
            .replace("\n", " ")\
            .replace("\r", "")

    try:
        skills = Skills.objects.get(resume=user_resume)
        skills.skills = convert_html_to_latex(skills.skills, theme_detail.theme)\
            .replace("\n", " ")\
            .replace("\r", "\n")
    except Skills.DoesNotExist:
        skills = None

    try:
        language = Languages.objects.get(resume=user_resume)
        language.languages = convert_html_to_latex(language.languages, theme_detail.theme)\
            .replace("\n", " ")\
            .replace("\r", "\n")
    except Languages.DoesNotExist:
        language = None

    award_set = Award.objects.filter(resume=user_resume)
    for elem in award_set:
        elem.award_summary = convert_html_to_latex(elem.award_summary, theme_detail.theme)\
            .replace("\n", " ")\
            .replace("\r", "")

    rendered = render_to_string('themes/{}.html'.format(theme_detail.theme),
                                {
                                    'theme_details': theme_detail,
                                    'personal': app_user,
                                    'educations': education_set,
                                    'works': work_set,
                                    'skills': skills,
                                    'summary': user_summary,
                                    'languages': language,
                                    'awards': award_set
                                })

    s = rendered[902:905]

    with open('output.tex', 'w', encoding="utf-8") as f:
        f.write(rendered)

    p = subprocess.Popen(["xelatex", "-interaction=scrollmode", "output.tex"])
    p.communicate()

    # Rename output.pdf to @resume_name.pdf
    resume_name = "{}.pdf".format(user_resume.name)
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
            return render(request, 'publish/preview.html', {'form': form,
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


def convert_html_to_latex(html, theme_id):
    """Convert html to latex based on theme"""

    if theme_id == "2":
        return html_to_latex(html)

    html = html.replace("</p>\r\n\r\n<p>", "\\\\")
    html = html.replace("</p>\n\n<p>", "\\\\")
    html = html.replace("</ol>", "\\end{enumerate} ")
    html = html.replace("</ul>", "\\end{itemize} ")

    html = html.replace("<li>", "\\item ")
    html = html.replace("</li>", " ")
    html = html.replace("<p>", " ")

    html = html.replace("<strong>", "\\textbf{")
    html = html.replace("</strong>", "} ")
    html = html.replace("<em>", "\\textit{")
    html = html.replace("</em>", "} ")
    html = html.replace("<u>", "\\underline{")
    html = html.replace("</u>", "} ")

    html = html.replace("&nbsp;", " ")

    if theme_id in ["1", "3", "4", "5", "6"]:
        html = html.replace("<ol>", "\\begin{enumerate} \n\\setlength\\itemsep{0pt}")
        html = html.replace("<ul>", "\\begin{itemize} \n\\setlength\\itemsep{0pt}")

        html = html.replace("</p>", " \\\\[-5pt]")

    return html

