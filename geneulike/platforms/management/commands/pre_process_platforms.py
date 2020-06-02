from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from datetime import timedelta
from geneulike.platforms.models import Platform

import requests, json

import sys


def extract_info():
    # We can use JSON for less than 500 record, so we need to make 50 time the request I guess
    max_data = 500
    ncbi_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=GPL[ETYP]&retmax={}&usehistory=y&retmode=json".format(str(max_data))
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
        custom_url = ncbi_url + "&retstart=" + str(current_count)
        if not r.status_code == 200:
            print("Error: response code for esearch is : " + r.status_code)
            return
        data = json.loads(r.content)
        _process_data(data["esearchresult"]['querykey'], data["esearchresult"]['webenv'], max_data)
        current_count += max_data
        i += 1

def _process_data(query_key, web_env, max_data=500):

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&version=2.0&query_key={}&WebEnv={}&retmode=json&retmax={}".format(query_key, web_env, max_data)
    r = requests.get(url)
    if not r.status_code == 200:
        print("Error: response code for esearch is : " + r.status_code)
        return
    data = json.loads(r.content)
    platform_list = []

    for id, platform in data['result'].items():
        if Platform.objects.filter(geo_uid=platform["uid"]).count() == 0:
            continue

        if id == "uids":
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
        extract_info()
