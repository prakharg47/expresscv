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
            attrs={'class': 'form-control', 'placeholder': 'Resume Name', }
        )
    )

    class Meta:
        model = Resume
        fields = ['name', ]

    def clean(self):
        if self.cleaned_data.get('name') == 'Prakhar':
            raise ValidationError("Invalid name")

        return self.cleaned_data


class PersonalForm(forms.ModelForm):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name', }
        )
    )

    email = forms.CharField(
        required=False,
        label="Email",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email', }
        )
    )

    mobile = forms.CharField(
        required=False,
        label="Mobile",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Mobile', }
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

    linkedin_url = forms.CharField(
        required=False,
        label="LinkedIn Url",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'LinkedIn url', }
        )
    )

    # photo = forms.FileField(
    #     required=False,
    #     label='Upload Image'
    # )

    class Meta:
        model = Personal
        # fields = ['name', 'email', 'mobile', 'city', 'country', 'linkedin_url', 'photo']
        fields = ['name', 'email', 'mobile', 'city', 'country', 'linkedin_url']


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
        label="From year",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '2018', }
        )
    )

    to_year = forms.CharField(
        required=False,
        label="To year",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '2018', }
        )
    )

    work_summary = forms.CharField(
        label="Summary",
        widget=CKEditorWidget()
    )

    class Meta:
        model = Work
        fields = ['company', 'designation', 'city', 'country', 'from_year', 'to_year', 'work_summary']



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
        model = Theme_Model
        fields = ['theme', 'font_size', 'font_family', 'horizontal_margins', 'top_margin', 'bottom_margin']


class SkillsForm(forms.ModelForm):
    technical = forms.CharField(
        label="Technical Skills",
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Technical', }
        )
    )

    management = forms.CharField(
        label="Management Skills",
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Management', }
        )
    )

    class Meta:
        model = Skills
        fields = ['management', 'technical']


class LanguagesForm(forms.ModelForm):
    languages = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Languages', }
        )
    )

    class Meta:
        model = Languages
        fields = ['languages']


MONTH_CHOICE = [(e, e) for e in ["January","February","March",
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



