import sys
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import  User, Group
from django.conf import settings
from guardian.shortcuts import assign_perm, remove_perm, get_group_perms, get_user_perms
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from geneulike.series.models import Serie


class ConversionType(models.Model):

    CONVERSION_SUBTYPE = (
        ('default_conversion', 'Single column with gene ID'),
        ('file_conversion', 'Use a custom conversion file'),
    )

    FILE_TYPE = (
        ('GEO', 'GEO conversion file'),
        ('CUSTOM', 'Custom conversion file'),
    )

    GENE_FORMAT = (
        ('gene_id','Entrez gene ID'),
        ('locus_tag','Locus tag'),
        ('ensembl_id','Ensembl ID'),
        ('ensembl_transcript','Ensembl transcript'),
        ('ensembl_protein','Ensembl protein'),
        ('accession_transcript','Accession transcript'),
        ('accession_protein','Accession protein'),
        ('uniprot_id','Uniprot ID'),
        ('uniprot_accession','Uniprot accession'),
    )

    type = models.CharField(max_length=20, choices=CONVERSION_SUBTYPE, default="default_conversion")
    format = models.CharField(max_length=50, choices=GENE_FORMAT, default="gene_id")
    file_type = models.CharField(max_length=20, choices=FILE_TYPE, default="CUSTOM")
    geo_platform_id = models.CharField(max_length=20, blank=True, null=True)
    conversion_file = models.FileField(upload_to="gene_lists", blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')

class GeneList(models.Model):

    STATUS = (
        ("CONVERTED", "Converted"),
        ("PENDING", "Pending"),
        ("ERROR", "Error"),
        ("DEFAULT", "Default")
    )

    TYPES = (
        ("CONVERSION", "Need a conversion"),
        ("NO_CONVERSION", "No conversion needed"),
        ("OTHER", "Bypass conversion"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField("description", blank=True,null=True)
    type = models.CharField(max_length=20, choices=TYPES, default="CONVERSION")
    tsx_id = models.CharField(max_length=200)
    serie = models.ForeignKey(Serie, blank=True, null=True, on_delete=models.CASCADE, related_name='genelists')
    conversion_type = models.ForeignKey(ConversionType, blank=True, null=True, on_delete=models.CASCADE, related_name='genelists')
    organism = models.CharField(max_length=200)
    raw_file = models.FileField(upload_to="gene_lists", blank=True)
    converted_file = models.FileField(upload_to="gene_lists", blank=True)
    conversion_data = JSONField(null=True, blank=True, default=dict)
    status = models.CharField(max_length=20, choices=STATUS, default="DEFAULT")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=("user"))

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        self.tsx_id = "GULLIST" + str(self.id)
        super(Project, self).save()
