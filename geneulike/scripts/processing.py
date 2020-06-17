import os
import shutil
import time
import tempfile
from urllib.request import urlopen
from zipfile import ZipFile
import gzip
from ftplib import FTP, error_temp

from geneulike.genes.models import Gene

from geneulike.taskapp.celery import app
from django.conf import settings
from geneulike.jobs.models import Job

from django.core.files import File


@app.task(bind=True)
def download_platform_file(self, platform_id):

    from geneulike.platforms.models import Platform
    try:
        platform = Platform.objects.get(id=platform_id)
    except geneulike.platforms.models.DoesNotExist:
        raise Exception("Platform with id {} was not found".format(platform_id))

    if not platform.ftp:
        raise Exception("Platform does not have an ftp link")

    platform.download_id = self.request.id
    platform.save()

    ftp_base_url ="ftp.ncbi.nlm.nih.gov"
    ftp = FTP(ftp_base_url, timeout=180)
    ftp.login()

    with tempfile.TemporaryDirectory() as dirpath:
        with open(dirpath + "/tmpfile", "wb") as f:
            ftp.retrbinary("RETR " + platform.ftp, f.write)
        ftp.quit()
        platform.conversion_file.save("temp", File(dirpath + "/tmpfile"), save=True)


def convert_file(self, genelist_id):

    from geneulike.genelists.models import GeneList
    try:
        gene_list = GeneList.objects.get(id=genelist_id)
    except geneulike.genelists.models.DoesNotExist:
        raise Exception("Gene list with id {} was not found".format(genelist_id))

    # Do not convert
    if not gene_list.conversion_type:
        return

    if not gene_list.raw_file:
        return

    if gene_list.conversion_type.type == "default_conversion":
        data = _default_convert(gene_list)

    elif gene_list.conversion_type.type == "file_conversion" and gene_list.conversion_type.conversion_file:
        data = _file_convert(gene_list)
    else:
        raise Exception("Gene list with id {} is using a file_conversion, but has no conversion file".format(genelist_id))


def _default_convert(gene_list):
    
    converted_genes = set()
    conversion_type = gene_list.conversion_type.format

    count = 0
    # Need to manage array fields
    with open(gene_list.raw_file.path, 'r') as f:
        for line in f:
            count +=1
            genes = Gene.objects.filter(**{conversion_type:line.strip()})
            if genes.count() > 0:
                converted_genes.add(genes[0].gene_id)
    data = {
        "gene_list": converted_genes,
        "total_genes": count,
        "alert": ""
    }

def _file_convert(gene_list):

    converted_genes = set()
    conversion_type = gene_list.conversion_type.format

    pass    


