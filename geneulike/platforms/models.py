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

import subprocess
import os
import shutil

from geneulike.species.models import Species

def get_upload_path(instance, filename):
    path =  os.path.join("platforms/{}/{}/".format(instance.taxon, instance.id), "conversion_file.csv")
    return path

class Platform(models.Model):

    PLATFORM_TYPE = (
        ('GEO', 'GEO based platform'),
        ('CUSTOM', 'Platform with custom conversion file'),
    )

    title = models.CharField(max_length=200)
    geo_uid = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField("description", blank=True,null=True)
    type = models.CharField(max_length=100, choices=PLATFORM_TYPE, default="GEO")
    taxon = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='platforms')
    ftp = models.CharField(max_length=200, blank=True, null=True)
    conversion_file = models.FileField(upload_to=get_upload_path, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')

    def __str__(self):
        return self.title
