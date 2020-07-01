from django.urls import path
from geneulike.genelists import views


app_name = "genelists"
urlpatterns = [
    path('create/<int:serie_id>', views.genelist_create_form, name="genelist_create"),
]
