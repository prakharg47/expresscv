from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.forms.widgets import TextInput, Textarea
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
        label="Email",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email', }
        )
    )

    mobile = forms.CharField(
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
        label="City",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'City', }
        )
    )

    country = forms.CharField(
        label="Country",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Country', }
        )
    )

    linkedin_url = forms.CharField(
        required=False,
        label="Country",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'LinkedIn url', }
        )
    )

    photo = forms.FileField(
        required=False,
        label='Upload Image'
    )

    class Meta:
        model = Personal
        fields = ['name', 'email', 'mobile', 'city', 'country', 'linkedin_url', 'photo']


class SummaryForm(forms.ModelForm):
    summary = forms.CharField(
        label="Summary",
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Summary', }
        )
    )

    class Meta:
        model = Summary
        fields = ['summary', ]


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
        label="Foreign languages",
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Foreign Languages', }
        )
    )

    class Meta:
        model = Skills
        fields = ['languages']


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
                                                   'from_year': TextInput(
                                                       attrs={'class': 'form-control Default',
                                                              'placeholder': 'From', }),
                                                   'to_year': TextInput(
                                                       attrs={'class': 'form-control Default', 'placeholder': 'To', })

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
                                       'work_summary': Textarea(
                                           attrs={'class': 'form-control', 'placeholder': 'Responsibilities', }),

                                       'city': TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'City', }),
                                       'country': TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Country', }),
                                       'from_year': AdminDateWidget(
                                           attrs={'class': 'form-control Default', 'placeholder': 'From', }),

                                       'to_year': TextInput(
                                           attrs={'class': 'form-control Default', 'placeholder': 'To', }),
                                   })

WorkFormset_extra1 = modelformset_factory(Work,
                                          exclude=('resume',), extra=1, max_num=6,
                                          widgets={
                                              'company': TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'Company', }),
                                              'designation': TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'Designation', }),
                                              'work_summary': Textarea(
                                                  attrs={'class': 'form-control', 'placeholder': 'Responsibilities', }),

                                              'city': TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'City', }),
                                              'country': TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'Country', }),
                                              'from_year': AdminDateWidget(
                                                  attrs={'class': 'form-control Default', 'placeholder': 'From', }),

                                              'to_year': TextInput(
                                                  attrs={'class': 'form-control Default', 'placeholder': 'To', }),
                                          })
