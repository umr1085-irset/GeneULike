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
from geneulike.genelists.models import GeneList
from django.contrib.postgres.forms import SimpleArrayField

class GeneListCreateForm(forms.ModelForm):


    class Meta:
        model = GeneList
        exclude = ["tsx_id", "serie", "converted_file", "converted_pickle_file", "conversion_data", "status", "created_at", "created_by", "updated_at", "geo_platform_id"]

    def __init__(self, *args, **kwargs):

        serie = kwargs.pop('serie')
        super(GeneListCreateForm, self).__init__(*args, **kwargs)
        
        SPECIES_CHOICES = (("", "---"),)
        for specie in serie.species:
            SPECIES_CHOICES += ((specie, specie),)

        PLATFORM_FILE_CHOICES = (("", "---"),)
        if serie.platforms:
            for platform in serie.platforms.all():
                if platform.ftp:
                    PLATFORM_FILE_CHOICES += ((platform.id, platform.geo_accession),)


        self.fields['species'] = form.ChoiceField(choices=SPECIES_CHOICES, required=False)
        self.fields['geo_file'] = form.ChoiceField(choices=PLATFORM_FILE_CHOICES, required=False)

        self.helper.layout = Layout(
            Fieldset(
                "General information regarding the Gene List",
                "title",
                "description",
                "species",
                "raw_file",
                "type"
            ),
            Div(
                HTML("Please select a GEO platform file"),
                "geo_file",
                style="display: none;",
                css_class="geo"
            ),
            Div(
                Div(
                    HTML("Select your curstom conversion file"),
                    "conversion_file",
                    style="display: none;",
                    css_class="custom"
                ),
                Div(
                    HTML("Please select a gene format"),
                    "format",
                    style="display: none;",
                    css_class="format"
                )
            )
        )

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save'))
