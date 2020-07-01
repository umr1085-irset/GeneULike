from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from geneulike.studies.models import Study

class StudyCreateForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ["title", "summary", "overall_design", "read_groups", "edit_groups"]
        labels = {
            "read_groups": "Groups with viewing permissions",
            "edit_groups": "Groups with editing permissions",
            "superproject": "Link this project to a superproject you own"
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.study = kwargs.pop('study', None)

        super(StudyCreateForm, self).__init__(*args, **kwargs)
        self.fields['read_groups'].help_text = "Groups with viewing permission on project and subentities. Will be ignored if the visibility is set to public. Use 'ctrl' to select multiple/unselect."
        self.fields['edit_groups'].help_text = "Groups with editing permission on project and subentities. Use 'ctrl' to select multiple/unselect."

        # TODO : Give link to group creation interface?
        groups = self.user.groups.all()
        self.fields['read_groups'].queryset = groups
        self.fields['edit_groups'].queryset = groups

        # To clone
        if self.study:
            self.fields['title'].initial = self.study.title
            self.fields['summary'].initial = self.study.summary
            self.fields['overall_design'].initial = self.study.overall_design

            if all([group in groups for group in self.study.read_groups.all()]):
                self.fields['read_groups'].initial = self.study.read_groups.all()

            if all([group in groups for group in self.study.edit_groups.all()]):
                self.fields['edit_groups'].initial = self.study.edit_groups.all()

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save'))

    def is_valid(self):
        valid = super(StudyCreateForm, self).is_valid()
        if not valid:
            return valid

        for edit_group in self.cleaned_data['edit_groups']:
            if edit_group not in self.cleaned_data['read_groups']:
                self.add_error("edit_groups", ValidationError(_('Groups with editing rights must also have reading rights'), code='invalid'))
                return False
        return True


class StudyEditForm(StudyCreateForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(StudyCreateForm, self).__init__(*args, **kwargs)
        self.fields['read_groups'].help_text = "Groups with viewing permission on project and subentities. Will be ignored if the visibility is set to public. Use 'ctrl' to select multiple/unselect"
        self.fields['edit_groups'].help_text = "Groups with editing permission on project and subentities. Use 'ctrl' to select multiple/unselect."

        # TODO : Give link to group creation interface?
        groups = self.user.groups.all()
        self.fields['read_groups'].queryset = groups
        self.fields['edit_groups'].queryset = groups

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save'))
