from dal import autocomplete
from django.db.models import Q

from geneulike.species.models import Species

class SpeciesAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Species.objects.all()
        values = set()
        for specie in qs:
            values.add(specie.name)
        values = list(values)
        if self.q:
            values = [val for val in values if val.lower().startswith(self.q.lower())]
        return values

    def get_result_value(self, result):
        return result

    def get_result_label(self, result):
        return result
