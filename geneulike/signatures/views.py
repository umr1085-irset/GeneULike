from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from guardian.mixins import PermissionRequiredMixin

from toxsign.projects.views import check_view_permissions
from toxsign.projects.models import Project
from toxsign.assays.models import Assay, Factor
from toxsign.signatures.models import Signature
from toxsign.signatures.forms import SignatureCreateForm, SignatureEditForm

from toxsign.projects.documents import ProjectDocument
from toxsign.signatures.documents import SignatureDocument
from elasticsearch_dsl import Q as Q_es

from dal import autocomplete
from django.db.models import Q

class SignatureToolAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                groups = [group.id for group in self.request.user.groups.all()]
                q = Q_es("match", created_by__username=self.request.user.username)  | Q_es("match", status="PUBLIC") | Q_es('nested', path="read_groups", query=Q_es("terms", read_groups__id=groups))
            else:
                q = Q_es("match", status="PUBLIC")
            allowed_projects =  ProjectDocument.search().sort('id').query(q).scan()
            # Limit all query to theses projects
            allowed_projects_id_list = [project.id for project in allowed_projects]
            docs = Q_es("match", down_gene_number=0) & Q_es("match", up_gene_number=0)
            qs = SignatureDocument.search().sort('id').filter("terms", factor__assay__project__id=allowed_projects_id_list).exclude(docs)
            query = self.q
            if query:
                query = "*" + query + "*"
                qs = qs.query(Q_es("query_string", query=query))
            return qs
        # Fall back to DB search if failure for any reason
        except Exception as e:
            raise e
            qs = Signature.objects.all()
            if query:
                qs = qs.filter(Q(tsx_id__istartswith=query))
        return qs

    def get_result_value(self, result):
        return result.id

    def get_result_label(self, result):
        return result.tsx_id + " - " + result.name

def DetailView(request, sigid):

    signature = get_object_or_404(Signature, tsx_id=sigid)

    return render(request, 'signatures/details.html', {'signature': signature})
