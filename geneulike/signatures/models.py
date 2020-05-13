from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import  User, Group
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver

import os
import shutil
import time

from django.core.files import File
from toxsign.genes.models import Gene
from toxsign.ontologies.models import Biological, Cell, CellLine, Chemical, Disease, Experiment, Species, Tissue
from toxsign.jobs.models import Job

import tempfile
from django.db.models import Q
from toxsign.taskapp.celery import app

class Signature(models.Model):
    DEVELOPPMENTAL_STAGE = (
        ("FETAL", 'Fetal'),
        ("EMBRYONIC", "Embryonic"),
        ("LARVA", "Larva"),
        ("NEONATAL", "Neo-natal"),
        ("JUVENILE", "Juvenile"),
        ("PREPUBERTAL", "Prepubertal"),
        ("ADULTHOOD", "Adulthood"),
        ("ELDERLY", "Elderly"),
        ("NA", "Na"),
        ("OTHER", "Other"),
    )
    GENERATION = (
        ('NA', 'NA'),
        ('F0', 'F0'),
        ('F1', 'F1'),
        ('F2', 'F2'),
        ('F3', 'F3'),
        ('F4', 'F4'),
        ('F5', 'F5'),
    )
    SEX_TYPE = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('BOTH', 'Both'),
        ("NA", "Na"),
        ("OTHER", "Other"),
    )

    SIGNATURE_TYPE = (
        ('GENOMICS', 'Genomics'),
        ('METABOLOMICS', 'Metabolomics'),
        ('TRANSCRIPTOMICS', 'Transcriptomics'),
        ('EPIGENOMICS', 'Epigenomics'),
        ('PROTEOMICS', 'Proteomics'),
    )

    GENE_ID = (
        ('ENTREZ', 'Entrez genes'),
        ('ENSEMBL', 'Ensembl'),
    )

    EXPERIMENTAL_TYPE = (
        ('EXVIVO', 'Ex-vivo'),
        ('INVITRO', 'In-vitro'),
        ('INVIVO', 'In-vivo'),
        ("NA", "Na"),
        ("OTHER", "Other"),
    )

    name = models.CharField(max_length=200)
    tsx_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=("user"))
    signature_type = models.CharField(max_length=20, choices=SIGNATURE_TYPE, default="GENOMICS")
    phenotype_description = models.TextField("Phenotype description", blank=True, null=True)
    experimental_design = models.TextField("Experimental design", blank=True, null=True)
    dev_stage = models.CharField(max_length=50, choices=DEVELOPPMENTAL_STAGE, default="NA")
    generation = models.CharField(max_length=10, choices=GENERATION, default="F0")
    sex_type = models.CharField(max_length=10, choices=SEX_TYPE, default="MALE")
    exp_type = models.CharField(max_length=10, choices=EXPERIMENTAL_TYPE, default="NA")
    organism = models.ForeignKey(Species, blank=True, null=True, on_delete=models.CASCADE, related_name='signature_used_in')
    tissue = models.ForeignKey(Tissue, blank=True, null=True, on_delete=models.CASCADE, related_name='signature_used_in')
    cell = models.ForeignKey(Cell, blank=True, null=True, on_delete=models.CASCADE, related_name='signature_used_in')
    cell_line = models.ForeignKey(CellLine, blank=True, null=True, on_delete=models.CASCADE, related_name='signature_used_in')
    cell_line_slug = models.CharField(max_length=200, blank=True, null=True)
    chemical = models.ForeignKey(Chemical, blank=True, null=True, on_delete=models.CASCADE, related_name='signature_used_in')
    chemical_slug = models.CharField(max_length=200, blank=True, null=True)
    disease = models.ForeignKey(Disease, blank=True, null=True, on_delete=models.CASCADE, related_name='signature_used_in')
    technology = models.ForeignKey(Experiment, blank=True, null=True, on_delete=models.CASCADE, related_name='signature_used_in')
    technology_slug = models.CharField(max_length=200, blank=True, null=True)
    platform = models.CharField(max_length=200, blank=True, null=True)
    control_sample_number = models.IntegerField(null=True, blank=True, default=0)
    treated_sample_number = models.IntegerField(null=True, blank=True, default=0)
    pvalue = models.FloatField(null=True, blank=True, default=None)
    cutoff = models.FloatField(null=True, blank=True, default=None)
    statistical_processing = models.TextField("Statistical processing", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('signatures:detail', kwargs={"sigid": self.tsx_id})

    def __init__(self, *args, **kwargs):
        super(Signature, self).__init__(*args, **kwargs)

    # Override save method to auto increment tsx_id
    def save(self, *args, **kwargs):
        if not self.tsx_id:
            self.tsx_id = "TSS" + str(self.id)
        super(Signature, self).save(*args, **kwargs)
        # Hacky Hacky
