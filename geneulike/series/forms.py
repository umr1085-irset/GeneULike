from dal import autocomplete
from django import forms
from crispy_forms.helper import FormHelper
from operator import itemgetter
from crispy_forms.layout import Submit, Layout, Row, Column, HTML, Button, Fieldset
from crispy_forms.bootstrap import FormActions, InlineField, StrictButton
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from geneulike.series.models import Serie
from geneulike.platforms.models import Platform


from django.contrib.postgres.forms import SimpleArrayField, SplitArrayField

class SerieCreateForm(forms.ModelForm):

    species = autocomplete.Select2ListCreateChoiceField(
                required=False,
                widget=autocomplete.TagSelect2(url='/species/autocomplete', attrs={"data-tags":"true", "data-html":True})
              )

    platforms = forms.ModelMultipleChoiceField(
                    queryset=Platform.objects.all(),
                    required=False,
                    widget=autocomplete.ModelSelect2Multiple(url='/platforms/autocomplete')
            )

    contributors = SimpleArrayField(forms.CharField(), required=False)
    technologies = SimpleArrayField(forms.CharField(), required=False)
    pubmed_ids = SimpleArrayField(forms.CharField(), required=False)
    cross_links = SimpleArrayField(forms.CharField(), required=False)

    class Meta:
        model = Serie
        fields = ["title", "summary", "overall_design", "contributors", "technologies", "pubmed_ids", "cross_links", "species"]

    def __init__(self, *args, **kwargs):

        self.serie = kwargs.pop('serie', None)
        super(SerieCreateForm, self).__init__(*args, **kwargs)

        # To clone
        if self.serie:
            self.fields['title'].initial = self.study.title
            self.fields['summary'].initial = self.study.summary
            self.fields['overall_design'].initial = self.study.overall_design
            self.fields['contributors'].initial = self.study.contributors
            self.fields['technologies'].initial = self.study.technologies
            self.fields['pubmed_ids'].initial = self.study.pubmed_ids
            self.fields['cross_links'].initial = self.study.cross_links
            self.fields['species'].initial = self.study.species

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save'))

    def clean_species(self):
        return self.cleaned_data['species'].split(",")
