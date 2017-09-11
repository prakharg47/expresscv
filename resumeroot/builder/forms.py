from crispy_forms.layout import Submit, Layout
from django import forms
from django.forms import ModelForm, inlineformset_factory
from crispy_forms.helper import FormHelper

from builder.models import ResumeConfig
from builder.models import Education


# class PersonalForm(forms.Form):
#     name = forms.CharField(max_length=50)
#     mobile = forms.IntegerField(widget=forms.NumberInput)
#     email = forms.EmailField(widget=forms.EmailInput)
#     summary = forms.CharField(widget=forms.Textarea)
#
#
# class EducationForm(forms.Form):
#     college = forms.CharField(max_length=50)
#     degree = forms.CharField(max_length=50)
#     gpa = forms.CharField(max_length=50)


class ResumeForm(ModelForm):
    class Meta:
        model = ResumeConfig
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-resumeform'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'builder'
        self.helper.form_tag = False

        # self.helper.add_input(Submit('submit', 'Submit'))


class EducationFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(EducationFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.form_tag = False

EducationFormSet = inlineformset_factory(ResumeConfig, Education,
                                         extra=2, form=ResumeForm, can_delete=True)




