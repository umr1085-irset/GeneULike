import sys
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import  User, Group
from django.conf import settings
from django_better_admin_arrayfield.models.fields import ArrayField

from guardian.shortcuts import assign_perm, remove_perm, get_group_perms, get_user_perms
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from geneulike.studies.models import Study
from geneulike.platforms.models import Platform


import subprocess
import os
import shutil

class Serie(models.Model):

    title = models.CharField(max_length=200)
    tsx_id = models.CharField(max_length=200)
    summary = models.TextField("summary", blank=True,null=True)
    overall_design = models.TextField("overall_design", blank=True,null=True)
    # Not fond of using user ids for contributors
    contributors =  ArrayField(models.CharField(max_length=200, blank=True), default=list)
    technologies = ArrayField(models.CharField(max_length=200, blank=True), default=list)
    platforms = models.ManyToManyField(Platform, blank=True, related_name="series")
    # Array field maybe? or comma separated?
    pubmed_ids =  ArrayField(models.CharField(max_length=30, blank=True), default=list)
    cross_links =  ArrayField(models.CharField(max_length=200, blank=True), default=list)
    species = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    study = models.ForeignKey(Study, blank=True, null=True, on_delete=models.CASCADE, related_name="series")
    ancestor = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="subseries_full")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="subseries")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=("user"))

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super(Serie, self).__init__(*args, **kwargs)
        self.initial_species = self.species

    # Override save method to auto increment tsx_id and parent/ancestors
    def save(self, *args, **kwargs):
        super(Serie, self).save(*args, **kwargs)
        self.tsx_id = "GULSER" + str(self.id)
        if not self.ancestor:
            if self.parent:
                if self.parent.ancestor:
                    self.ancestor = self.parent.ancestor
                else:
                    self.ancestor = self.parent
        super(Serie, self).save()
        sync_data(self)

# TODO: Make async call 
def sync_data(serie):
    # First identify the study
    if serie.study:
        study = serie.study
    else:
        study = serie.ancestor.study

    species = set()
    contributors = set()
    cross_links = set()
    technologies = set()
    pubmed_ids = set()

    for series in study.series.all():
        species |= set(series.species)
        contributors |= set(series.contributors)
        cross_links |= set(series.cross_links)
        technologies |= set(series.technologies)
        pubmed_ids |= set(series.pubmed_ids)

        if series.subseries_full:
            for subseries in series.subseries_full.all():
                species |= set(subseries.species)
                contributors |= set(subseries.contributors)
                cross_links |= set(subseries.cross_links)
                technologies |= set(subseries.technologies)
                pubmed_ids |= set(subseries.pubmed_ids)

    study.species = list(species)
    study.contributors = list(contributors)
    study.cross_links = list(cross_links)
    study.technologies = list(technologies)
    study.pubmed_ids = list(pubmed_ids)
    study.save()
