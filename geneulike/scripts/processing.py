import os
import shutil
import time
import tempfile
import pickle
from urllib.request import urlopen
from zipfile import ZipFile
import gzip
from ftplib import FTP, error_temp

from geneulike.genes.models import Gene

from geneulike.taskapp.celery import app
from django.conf import settings
from geneulike.jobs.models import Job
from django.core.files import File

from django.db.models import Q

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

@app.task(bind=True)
def convert_file(self, genelist_id):

    from geneulike.genelists.models import GeneList
    try:
        gene_list = GeneList.objects.get(id=genelist_id)
    except geneulike.genelists.models.DoesNotExist:
        raise Exception("Gene list with id {} was not found".format(genelist_id))

    # Do not convert

    if not gene_list.raw_file:
        return

    if gene_list.type == "no_conversion":
        gene_list.status = "NO_CONVERSION"
        gene_list.save()
        return

    gene_list.status = "PENDING"
    gene_list.save()

    if gene_list.type == "default_conversion":
        data = _default_convert(gene_list)

    elif gene_list.type == "geo_file_conversion":
        if gene_list.geo_platform_id:
            data = _geo_file_convert(gene_list)
        else:
            raise Exception("Gene list with id {} is using a geo conversion, but has no geo file associated file".format(genelist_id))
    else:
        if gene_list.conversion_file
            data = _file_convert(gene_list)
        else:
            raise Exception("Gene list with id {} is using a file conversion, but has no conversion file".format(genelist_id))

    ratio = len(data["gene_list"]) / data["total_genes"]
    data = {"converted_genes": len(data["gene_list"]), "raw_genes": data["total_genes"]}

    if ratio < 0.5:
        gene_list.status = "WARNING"
        data["warning"] = "Less than 50% of genes were converted."
    else:
        gene_list.status = "CONVERTED"

    _save_converted_file(gene_list, data)

    gene_list.conversion_data = data
    gene_list.save()


def _default_convert(gene_list):
    
    converted_genes = set()
    conversion_type = gene_list.format

    count = 0
    # Need to manage array fields
    with open(gene_list.raw_file.path, 'r') as f:
        for line in f:
            count +=1
            if conversion_type == "gene_id":
                genes = Gene.objects.filter(Q(gene_id=line.strip()) | Q(discontinued_gene_ids__contains=line.strip()))
            else:
                genes = Gene.objects.filter(**{conversion_type:line.strip()})
            if genes.count() > 0:
                converted_genes.add(genes[0].gene_id)
    data = {
        "gene_list": converted_genes,
        "total_genes": count,
        "alert": ""
    }

def _geo_file_convert(gene_list):

    from geneulike.platforms.models import Platform
    converted_genes = set()

    platform = Platform.objects.get(id=gene_list.geo_platform_id)
    # Possible infinite loop... set max timeout and mail admin?
    if platform.conversion_file:
        file_path = platform.conversion_file.path
    else:
        if platform.download_id:
            time.sleep(200)
            return _geo_file_convert(gene_list)
        else:
            download_platform_file.delay(platform.id)
            time.sleep(200)
            return _geo_file_convert(gene_list)
    conversion_dict = {}

    with open(file_path, 'r') as f:
        for line in f:
            #Skip comments and column names
            if line.startswith("#") or line.startswith("!") or line.startswith("^") or line.startswith("ID\tGene title"):
                continue
            line = line.split("\t")
            conversion_dict[line[0].strip()] = line[3].strip()

    count = 0
    with open(gene_list.raw_file.path, 'r') as f:
        for line in f:
            count +=1
            if line.strip() in conversion_dict:
                converted_genes.add(conversion_dict[line.strip()])

    data = {
        "gene_list": converted_genes,
        "total_genes": count,
        "alert": ""
    }

def _file_convert(gene_list):

    from geneulike.platforms.models import Platform
    converted_genes = set()
    conversion_type = gene_list.format

    file_path = gene_list.conversion_file.path
    conversion_dict = {}

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("#") or line.startswith("!") or line.startswith("^"):
                continue
            line = line.split("\t")
            if gene_list.format == "gene_id":
                genes = Gene.objects.filter(Q(gene_id=line[1].strip()) | Q(discontinued_gene_ids__contains=line[1].strip()))
            else:
                genes = Gene.objects.filter(**{gene_list.format:line[1].strip()})
            if genes.count() > 0:
                conversion_dict[line[0].strip()] = genes[0].gene_id

    count = 0
    with open(gene_list.raw_file.path, 'r') as f:
        for line in f:
            count +=1
            if line.strip() in conversion_dict:
                converted_genes.add(conversion_dict[line.strip()])

    data = {
        "gene_list": converted_genes,
        "total_genes": count,
        "alert": ""
    }


def _save_converted_file(gene_list, data)

    with tempfile.TemporaryDirectory() as dirpath:
        with open(dirpath + "/tmpfile", "w") as f:
            f.write("\n".join(data['gene_list']))

        with open(dirpath + "/tmpfile.pickle", "wb") as f:
            pickle.dump(data[gene_list], f)

        gene_list.converted_file.save("temp", File(dirpath + "/tmpfile"), save=True)
        gene_list.converted_file.save("temp", File(dirpath + "/tmpfile.pickle"), save=True)
