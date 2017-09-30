from crispy_forms.layout import Submit, Layout
from django import forms
from django.forms import ModelForm, inlineformset_factory, modelformset_factory
from crispy_forms.helper import FormHelper

from .models import *

class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['name', 'email', 'mobile', 'summary', 'city', 'country']


EducationFormset = modelformset_factory(Education,
                                        exclude=('user',),
                                        extra=1,
                                        max_num=4)

WorkFormset = modelformset_factory(Work,
                                   exclude=('user',),
                                   extra=1,
                                   max_num=6)

