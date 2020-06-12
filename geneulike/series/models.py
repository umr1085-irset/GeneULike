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

from geneulike.studies.models import Study

import subprocess
import os
import shutil

class Study(models.Model):

    title = models.CharField(max_length=200)
    tsx_id = models.CharField(max_length=200)
    summary = models.TextField("summary", blank=True,null=True)
    overall_design = models.TextField("overall_design", blank=True,null=True)
    # Not fond of using user ids for contributors
    contributors = models.TextField("contributors", blank=True,null=True)
    # Array field maybe? or comma separated?
    pubmed_ids = models.TextField("pubmed_ids", blank=True,null=True)
    cross_link = models.TextField("cross_link", blank=True, null=True)
    study = models.ForeignKey(Study, blank=True, null=True, on_delete=models.CASCADE, related_name="series")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="subseries")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=("user"))

    def __str__(self):
        return self.name

    # Override save method to auto increment tsx_id
    # Also set permissions for owner on item
    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        self.tsx_id = "GULSER" + str(self.id)
        super(Project, self).save()
