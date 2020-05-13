from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from toxsign.signatures.models import Signature
class SignatureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name',
        'created_by',
        'tsx_id',
        'signature_type',
        'phenotype_description',
        'experimental_design',
        'dev_stage',
        'generation',
        'sex_type',
        'exp_type',
        'organism',
        'tissue',
        'cell',
        'cell_line',
        'chemical',
        'chemical_slug',
        'disease',
        'technology',
        'technology_slug',
        'platform',
        'control_sample_number',
        'treated_sample_number',
        'pvalue',
        'cutoff',
        'statistical_processing',
    ]}),
    ]
    list_display = ['name', 'created_at', 'updated_at']
    autocomplete_fields = ['disease','organism','cell', 'tissue', 'cell', 'cell_line', 'technology', 'chemical']
    search_fields = ['name']

admin.site.register(Signature, SignatureAdmin)
