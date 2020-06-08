import sys
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import  User, Group
from django.conf import settings

class Species(models.Model):

    name = models.CharField(max_length=200)
    species_id = models.CharField(max_length=20)

    def __str__(self):
        return self.name
