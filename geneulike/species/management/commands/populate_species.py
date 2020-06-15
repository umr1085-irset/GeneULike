from django.core.management.base import BaseCommand, CommandError

from geneulike.species.models import Species
from geneulike.users.models import User
from django.conf import settings

def populate_species():

    species = {
        'Homo sapiens': '9606',
        'Macaca mulatta': '9544',
        'Mus musculus': '10090',
        'Rattus norvegicus': '10116',
        'Canis lupus familiaris': '9615',
        'Bos taurus': '9913',
        'Sus scrofa': '9823',
        'Gallus gallus': '9031',
        'Danio rerio': '7955',
        'Xenopus laevis': "8355",
        "Takifugu rubripes": "31033",
        "Caenorhabditis elegans": "6239",
        "Arabidopsis thaliana": "3702",
        "Saccharomyces cerevisiae": "4932"
        }

    for key, value in species.items():
        species = Species.objects.filter(name=key)
        if not species:
            species = Species(name=key, species_id=value)
            species.save()

class Command(BaseCommand):
    help = 'Populate species'

    def handle(self, *args, **options):
        populate_species()
