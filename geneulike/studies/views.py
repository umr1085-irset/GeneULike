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

from geneulike.studies.models import Study

def study_create_form(request):
    if not request.user.is_authenticated:
        return redirect('/unauthorized')

    data = {}
    if request.method == 'POST':
        form = forms.StudyCreateForm(request.POST, user=request.user)
        if form.is_valid():
            object = form.save(commit=False)
            object.created_by = request.user
            object.save()
            
            return redirect(reverse("home"))
        else:
            data['form_is_valid'] = False
    else:
        form = forms.StudyCreateForm(user=request.user)

    context = {'form': form}
    return render(request, 'studies/entity_create.html', context)
