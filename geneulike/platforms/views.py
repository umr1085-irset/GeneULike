from dal import autocomplete
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps

from geneulike.platforms.models import Platform

class PlatformAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        query = self.q
        qs = Platform.objects.all()
        if query:
            qs = qs.filter(Q(title__istartswith=query) | Q(geo_accession__istartswith=query))
        return qs

    def get_result_label(self, result):
        return "[{}] {}".format(result.geo_accession, result.title)
