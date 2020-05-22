from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from datetime import timedelta
from geneulike.platforms.models import Platform

import requests, json

import sys


def extract_info():
    # We can use JSON for less than 500 record, so we need to make 50 time the request I guess
    ncbi_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=GPL[ETYP]&retmax=500&usehistory=y&retmode=json"
    r = requests.get(ncbi_url)
    if not r.status_code == 200:
        print("Error: response code for esearch is : " + r.status_code)
        return

    data = json.loads(r.body)
    total_count = int(data["esearchresult"]["count"])
    iterations = total_count//500
    _process_data(data["esearchresult"]['querykey'], data["esearchresult"]['webenv'])
    current_count = 500
    i = 0
    while i < iterations:
        custom_url = ncbi_url + "&retstart=" + current_count
        if not r.status_code == 200:
            print("Error: response code for esearch is : " + r.status_code)
            return
        data = json.loads(r.body)
        _process_data(data["esearchresult"]['querykey'], data["esearchresult"]['webenv'])
        current_count += 500
        i += 1

def _process_data(query_key, web_env):

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&version=2.0&query_key={}&WebEnv={}&retmode=json&retmax=500".format(query_key, web_env)
    r = requests.get(ncbi_url)
    if not r.status_code == 200:
        print("Error: response code for esearch is : " + r.status_code)
        return
    data = json.loads(r.body)
    platform_list = []

    for platform in data['result']:
        if Platform.objects.filter(geo_uid=platform["uid"]).count() == 0:
            continue

        dict = {
            "geo_uid": platform["uid"],
            "accession": platform["accession"],
            "title": platform["title"],
            "summary": platform["summary"],
            "taxon": platform["taxon"]
        }

        if platform["ftplink"]:
            dict["ftp"] = platform["ftplink"]

        platform_list.append(Platform(**dict))

    Platform.objects.bulk_create(platform_list)

class Command(BaseCommand):
    help = 'Extract info from GEO on all platforms'

    def handle(self, *args, **options):
        pass
