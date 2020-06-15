import json, os

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.conf import settings
from django.shortcuts import redirect

from elasticsearch_dsl import Q as Q_es

from django.template.loader import render_to_string
from . import forms
from django.http import JsonResponse
from django.http import FileResponse
from django.utils.functional import LazyObject

class SearchResults(LazyObject):
    def __init__(self, search_object):
        self._wrapped = search_object

    def __len__(self):
        return self._wrapped.count()

    def __getitem__(self, index):
        search_results = self._wrapped[index]
        if isinstance(index, slice):
            search_results = list(search_results)
        return search_results

def HomeView(request):
        context = {}
        return render(request, 'pages/home.html',context)
