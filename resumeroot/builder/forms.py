from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory, Select
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

from .models import *


class ResumeForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Resume Name"),
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '', }
        )
    )

    class Meta:
        model = Resume
        # fields = ['name', 'tags']
        fields = ['name']

    def clean(self):
        if self.cleaned_data.get('name') == 'Prakhar':
            raise ValidationError("Invalid name")

        return self.cleaned_data


class PersonalForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Elon', }
        )
    )

    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Musk', }
        )
    )

    email = forms.CharField(
        required=False,
        label="Email",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'elon.musk@tesla.com', }
        )
    )

    mobile = forms.CharField(
        required=False,
        label="Mobile",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '+1 414 567890', }
        )
    )

    title = forms.CharField(
        required=False,
        label="Title ",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Rocket Scientist', }
        )
    )

    # summary = forms.CharField(
    #     label="Summary",
    #     widget=forms.Textarea(
    #         attrs={'class': 'form-control', 'placeholder': 'Summary', }
    #     )
    # )

    city = forms.CharField(
        required=False,
        label="City",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'California', }
        )
    )

    country = forms.CharField(
        required=False,
        label="Country",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'USA', }
        )
    )

    linkedin_url = forms.CharField(
        required=False,
        label="LinkedIn",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'linkedin.com/r/musk', }
        )
    )

    # photo = forms.FileField(
    #     required=False,
    #     label='Upload Image'
    # )

    class Meta:
        model = Personal
        # fields = ['name', 'email', 'mobile', 'city', 'country', 'linkedin_url', 'photo']
        fields = ['first_name', 'last_name', 'email', 'mobile', 'title', 'city', 'country', 'linkedin_url']


class SummaryForm(forms.ModelForm):
    summary = forms.CharField(
        label="Summary",
        widget=CKEditorWidget()
    )

    class Meta:
        model = Summary
        fields = ['summary', ]


class ExperienceForm(forms.ModelForm):
    company = forms.CharField(
        required=False,
        label="Company",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Google', }
        )
    )

    designation = forms.CharField(
        required=False,
        label="Designation",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Developer', }
        )
    )

    city = forms.CharField(
        required=False,
        label="City",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'City', }
        )
    )

    country = forms.CharField(
        required=False,
        label="Country",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Country', }
        )
    )

    from_year = forms.CharField(
        required=False,
        label="From",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Jan, 2016', }
        )
    )

    to_year = forms.CharField(
        required=False,
        label="To",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Mar, 2018 / present', }
        )
    )

    work_summary = forms.CharField(
        required=False,
        label="Summary",
        widget=CKEditorWidget()
    )

    class Meta:
        model = Work
        fields = ['company', 'designation', 'city', 'country', 'from_year', 'to_year', 'work_summary']


class EducationNewForm(forms.ModelForm):
    college = forms.CharField(
        required=False,
        label="College",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Harvard Business School', }
        )
    )

    major = forms.CharField(
        required=False,
        label="Major",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Chemical Engineering', }
        )
    )

    degree = forms.CharField(
        required=False,
        label="Degree",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Masters of Science', }
        )
    )

    gpa = forms.CharField(
        required=False,
        label="GPA",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '4.0', }
        )
    )

    city = forms.CharField(
        required=False,
        label="City",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Boston', }
        )
    )

    country = forms.CharField(
        required=False,
        label="Country",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'USA', }
        )
    )

    from_year = forms.CharField(
        required=False,
        label="From",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Jan, 2018', }
        )
    )

    to_year = forms.CharField(
        required=False,
        label="To",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Mar, 2018 / present', }
        )
    )

    education_summary = forms.CharField(
        required=False,
        label="Summary",
        widget=CKEditorWidget()
    )

    class Meta:
        model = Education
        fields = ['college', 'major', 'degree', 'gpa', 'city', 'country', 'from_year', 'to_year', 'education_summary']


class ThemesModelForm(forms.ModelForm):
    # THEMES_CHOICES = [
    #     (0, 'standard'),
    #     (1, 'express'),
    #     (2, 'compact')
    # ]
    #
    # FONTS = [
    #     (0, 'computer modern'),
    #     (1, 'arial'),
    #     (2, 'calibri')
    # ]
    #
    # theme = forms.ChoiceField(THEMES_CHOICES, widget=forms.Select())
    # font_family = forms.ChoiceField(FONTS, widget=forms.Select())

    class Meta:
        model = Theme
        fields = ['theme', 'font_size', 'font_family', 'horizontal_margins', 'top_margin', 'bottom_margin']

class ThemesChoiceForm(forms.Form):

    choices = Theme.THEME_CHOICES
    theme_name = forms.CharField(label='Choose your theme', widget=forms.RadioSelect(choices=choices))



class AwardForm(forms.ModelForm):
    award_name = forms.CharField(
        label="Award/Certificate",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Company Secretary', }
        )
    )

    organisation = forms.CharField(
        label="Organisation",
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Indian Company Secretary Institute', }
        )
    )

    year = forms.CharField(
        required=False,
        label="Year",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '2015', }
        )
    )

    award_summary = forms.CharField(
        required=False,
        label="Short Description",
        widget=CKEditorWidget()
    )

    class Meta:
        model = Award
        fields = ['award_name', 'organisation', 'year', 'award_summary']


class SkillsForm(forms.ModelForm):
    skills = forms.CharField(
        label="Skills",
        widget=CKEditorWidget()
    )

    class Meta:
        model = Skills
        fields = ['skills']


class LanguagesForm(forms.ModelForm):
    languages = forms.CharField(
        label="Languages",
        widget=CKEditorWidget()
    )

    class Meta:
        model = Languages
        fields = ['languages']


MONTH_CHOICE = [(e, e) for e in ["January", "February", "March",
                                 "April", "May", "June", "July", "August",
                                 "September", "October", "November", "December"]]

EducationFormset_extra1 = modelformset_factory(Education,
                                               exclude=('resume',), extra=1, max_num=4,
                                               widgets={
                                                   'college': TextInput(
                                                       attrs={'class': 'form-control', 'placeholder': 'College', }),
                                                   'gpa': TextInput(
                                                       attrs={'class': 'form-control', 'placeholder': 'GPA', }),
                                                   'degree': TextInput(
                                                       attrs={'class': 'form-control', 'placeholder': 'Degree', }),
                                                   'major': TextInput(
                                                       attrs={'class': 'form-control', 'placeholder': 'Major', }),
                                                   'city': TextInput(
                                                       attrs={'class': 'form-control', 'placeholder': 'City', }),
                                                   'country': TextInput(
                                                       attrs={'class': 'form-control', 'placeholder': 'Country', }),
                                                   'from_year': Select(choices=MONTH_CHOICE,
                                                                       attrs={'class': 'form-control',
                                                                              'placeholder': 'From Year', }

                                                                       ),
                                                   'from_month': Select(choices=MONTH_CHOICE,
                                                                        attrs={'class': 'form-control',
                                                                               'placeholder': 'From Year', }

                                                                        ),
                                                   'to_year': TextInput(
                                                       attrs={'class': 'form-control', 'placeholder': 'To Year', }),
                                                   'to_month': Select(choices=MONTH_CHOICE,
                                                                      attrs={'class': 'form-control',
                                                                             'placeholder': 'From Year', }

                                                                      )
                                               })

EducationFormset = modelformset_factory(Education,
                                        exclude=('resume',), extra=0, max_num=4,
                                        widgets={
                                            'college': TextInput(
                                                attrs={'class': 'form-control', 'placeholder': 'College', }),
                                            'gpa': TextInput(attrs={'class': 'form-control', 'placeholder': 'GPA', }),
                                            'degree': TextInput(
                                                attrs={'class': 'form-control', 'placeholder': 'Degree', }),
                                            'major': TextInput(
                                                attrs={'class': 'form-control', 'placeholder': 'Major', }),
                                            'city': TextInput(
                                                attrs={'class': 'form-control', 'placeholder': 'City', }),
                                            'country': TextInput(
                                                attrs={'class': 'form-control', 'placeholder': 'Country', }),
                                            'from_year': TextInput(
                                                attrs={'class': 'form-control Default', 'placeholder': 'From', }),
                                            'to_year': TextInput(
                                                attrs={'class': 'form-control Default', 'placeholder': 'To', })

                                        })

WorkFormset = modelformset_factory(Work,
                                   exclude=('resume',), extra=0, max_num=6,
                                   widgets={
                                       'company': TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Company', }),
                                       'designation': TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Designation', }),
                                       # 'work_summary': Textarea(
                                       #     attrs={'class': 'form-control', 'placeholder': 'Responsibilities', }),

                                       'city': TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'City', }),
                                       'country': TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Country', }),
                                       'from_year': AdminDateWidget(
                                           attrs={'class': 'form-control Default', 'placeholder': 'From', }),

                                       'to_year': TextInput(
                                           attrs={'class': 'form-control Default', 'placeholder': 'To', }),
                                       'work_summary': CKEditorWidget(),
                                   })

WorkFormset_extra1 = modelformset_factory(Work,
                                          exclude=('resume',), extra=1, max_num=6,
                                          widgets={
                                              'company': TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'Company', }),
                                              'designation': TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'Designation', }),
                                              # 'work_summary': Textarea(
                                              #     attrs={'class': 'form-control', 'placeholder': 'Responsibilities', }),

                                              'city': TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'City', }),
                                              'country': TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'Country', }),
                                              'from_year': AdminDateWidget(
                                                  attrs={'class': 'form-control Default', 'placeholder': 'From', }),

                                              'to_year': TextInput(
                                                  attrs={'class': 'form-control Default', 'placeholder': 'To', }),
                                              'work_summary': CKEditorWidget(),
                                          })


class ThemesForm(forms.Form):
    CHOICES = [
        (0, 'standard'),
        (1, 'express'),
        (2, 'compact'),
        (3, 'modern')
    ]

    theme = forms.ChoiceField(choices=CHOICES)




class FineTuningForm(forms.Form):
    FONTS = [
        (0, 'computer modern'),
        (1, 'arial'),
        (2, 'calibri')
    ]
    font_size = forms.DecimalField(label='Font size')
    font_family = forms.ChoiceField(label='Font family', choices=FONTS)
    horizontal_margins = forms.DecimalField(label='Horizontal margin')
    top_margin = forms.DecimalField(label='Top margin')
    bottom_margin = forms.DecimalField(label='Bottom margin')
