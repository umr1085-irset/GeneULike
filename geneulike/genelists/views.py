import json, os

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.conf import settings
from django.shortcuts import redirect
from django.template.loader import render_to_string
from . import forms

from geneulike.series.models import Serie
from geneulike.platforms.models import Platform

def genelist_create_form(request, serie_id):
    if not request.user.is_authenticated:
        return redirect('/unauthorized')

    serie = get_object_or_404(Serie, id=serie_id)

    data = {}
    if request.method == 'POST':
        form = forms.GeneListCreateForm(request.POST, request.FILES, serie=serie)
        if form.is_valid():
            object = form.save(commit=False)
            if object.type == "geo_file_conversion":
                platform_id = form.cleaned_data['genes']
                object.geo_platform_id = platform_id
            object.serie = serie
            object.created_by = request.user
            object.save()
            return redirect(reverse("home"))
        else:
            data['form_is_valid'] = False
    else:
        form = forms.GeneListCreateForm(serie=serie)

    context = {'form': form}
    return render(request, 'genelists/entity_create.html', context)
