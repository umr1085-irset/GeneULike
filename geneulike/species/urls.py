from django.urls import path, re_path
from geneulike.species import views


app_name = "species"
urlpatterns = [
    re_path(r'^autocomplete/$', views.SpeciesAutocomplete.as_view(), name="species-autocomplete"),
]
