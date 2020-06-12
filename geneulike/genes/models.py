import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import  User, Group
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.apps import apps
from django.contrib.postgres.fields import ArrayField


class Gene(models.Model):

    gene_id =  models.CharField(max_length=50)
    tax_id =  models.CharField(max_length=50, blank=True)
    symbol =  models.CharField(max_length=50, blank=True)
    locus_tag = models.CharField(max_length=50, blank=True)
    synonyms =  models.TextField(blank=True)
    discontinued_gene_ids = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    ensembl_id =  models.CharField(max_length=50, blank=True)
    ensembl_transcript = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    ensembl_protein = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    accession_transcript = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    accession_protein = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    uniprot_accession = models.CharField(max_length=50, blank=True)
    uniprot_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.gene_id

