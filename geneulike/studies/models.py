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
from django_better_admin_arrayfield.models.fields import ArrayField

import subprocess
import os
import shutil

class Study(models.Model):
    AVAILABLE_STATUS = (
        ('PRIVATE', 'Private'),
        ('PENDING', 'Pending'),
        ('PUBLIC', 'Public'),
    )

    title = models.CharField(max_length=200)
    tsx_id = models.CharField(max_length=200)
    summary = models.TextField("summary", blank=True, null=True)
    overall_design = models.TextField("overall_design", blank=True, null=True)
    contributors =  ArrayField(models.CharField(max_length=50, blank=True), default=list)
    technologies =  ArrayField(models.CharField(max_length=50, blank=True), default=list)
    pubmed_ids =  ArrayField(models.CharField(max_length=50, blank=True), default=list)
    species = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    cross_links = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=("user"))
    read_groups = models.ManyToManyField(Group, blank=True, related_name='read_access_to')
    edit_groups = models.ManyToManyField(Group, blank=True, related_name='edit_access_to')
    status = models.CharField(max_length=20, choices=AVAILABLE_STATUS, default="PRIVATE")

    class Meta:
        permissions = (('view_study', 'View study'),)
        default_permissions = ('add', 'change', 'delete')

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Study, self).__init__(*args, **kwargs)
        self.initial_owner = self.created_by
        self.initial_status = self.status

    def save(self, *args, **kwargs):
        force = kwargs.pop('force', False)
        super(Study, self).save(*args, **kwargs)
        self.tsx_id = "GULSTUD" + str(self.id)
        super(Study, self).save()
        change_permission_owner(self)


# Need to add some checks (or catch exception) in case there is a disconnect between existing perm and groups
@receiver(m2m_changed, sender=Study.read_groups.through)
def update__permissions_read(sender, instance, action, **kwargs):
    if instance.read_groups.all():
        if action == 'pre_remove':
            for group in instance.read_groups.all():
                if 'view_Study' in get_group_perms(group, instance):
                    remove_perm('view_Study', group, instance)
        if action == 'post_add':
            for group in instance.read_groups.all():
                if 'view_Study' not in get_group_perms(group, instance):
                    assign_perm('view_Study', group, instance)

@receiver(m2m_changed, sender=Study.edit_groups.through)
def update__permissions_write(sender, instance, action, **kwargs):
    if instance.edit_groups.all():
        if action == 'pre_remove':
            for group in instance.edit_groups.all():
                if 'change_Study' in get_group_perms(group, instance):
                    remove_perm('change_Study', group, instance)
        if action == 'post_add':
            for group in instance.edit_groups.all():
                if 'change_Study' not in get_group_perms(group, instance):
                    assign_perm('change_Study', group, instance)

@receiver(models.signals.pre_delete, sender=Study)
def auto_delete_Study_on_delete(sender, instance, **kwargs):
    # Delete the folder
    local_path = "{}/".format(instance.tsx_id)
    unix_path = settings.MEDIA_ROOT + "/files/" + local_path
    if(os.path.exists(unix_path)):
        shutil.rmtree(unix_path)

def change_permission_owner(self):
    owner_permissions = ['view_study', 'change_study', 'delete_study']

    if self.initial_owner:
               # If update, remove permission, else do nothing
        if self.initial_owner != self.created_by:
            initial_owner_permission = get_user_perms(self.initial_owner, self)
            for permission in owner_permissions:
                if permission in initial_owner_permission:
                    remove_perm(permission, self.initial_owner, self)

    user_permissions = get_user_perms(self.created_by, self)
    for permission in owner_permissions:
        if permission not in user_permissions:
            assign_perm(permission, self.created_by, self)
