from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from datetime import timedelta
from geneulike.platforms.models import Platform
from geneulike.species.models import Species
from ftplib import FTP, error_temp
import requests, json

import sys

def extract_info(organism):
    # We can use JSON for less than 500 record, so we need to make 50 time the request I guess
    max_data = 500
    organism = organism.replace(" ", "+")
    ncbi_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=GPL[ETYP]{}[Organism]&retmax={}&usehistory=y&retmode=json".format(organism, str(max_data))
    r = requests.get(ncbi_url)
    if not r.status_code == 200:
        print("Error: response code for esearch is : " + r.status_code)
        return

    data = json.loads(r.content)
    total_count = int(data["esearchresult"]["count"])
    iterations = total_count//max_data
    _process_data(data["esearchresult"]['querykey'], data["esearchresult"]['webenv'], max_data)
    current_count = max_data
    i = 0
    while i < iterations:
        _process_data(data["esearchresult"]['querykey'], data["esearchresult"]['webenv'], max_data, current_count)
        current_count += max_data
        i += 1

def _process_data(query_key, web_env, max_data=500, current_count=0):

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&version=2.0&query_key={}&WebEnv={}&retmode=json&retmax={}&retstart={}".format(query_key, web_env, max_data, current_count)
    ftp_base_url ="ftp.ncbi.nlm.nih.gov"
    r = requests.get(url)
    if not r.status_code == 200:
        print("Error: response code for esearch is : " + r.status_code)
        return
    data = json.loads(r.content)
    platform_list = []

    ftp = FTP(ftp_base_url, timeout=180)
    ftp.login()

    for id, platform in data['result'].items():
        if not Platform.objects.filter(geo_uid=platform["uid"]).count() == 0:
            continue

        if id == "uids":
            continue

        dict_data = {
            "geo_uid": platform["uid"],
            "accession": platform["accession"],
            "title": platform["title"],
            "summary": platform["summary"],
            "taxon": platform["taxon"],
        }

        if platform["ftplink"]:
            ftp_url = platform["ftplink"].replace("ftp://", "").split("/")[1:]
            ftp_url = "/" + "/".join(ftp_url)

            annot_path = ftp_url + "annot"
            file_path = ftp_url + "annot/{}.annot.gz".format(platform["accession"])

            try:
                if file_path in ftp.nlst(annot_path):
                    dict_data['ftp'] = ftp_base_url + file_path
            except error_temp:
                pass

        platform_list.append(Platform(**dict_data))

    Platform.objects.bulk_create(platform_list,  batch_size=1000)

class Command(BaseCommand):
    help = 'Extract info from GEO on all platforms'

    def handle(self, *args, **options):
        species = Species.objects.all()
        if species.count == 0:
            print("No species found : skipping")
            return
        for specie_name in [specie.name for specie in species]:
            print("Parsing platforms for species " + specie_name)
            extract_info(specie_name)
