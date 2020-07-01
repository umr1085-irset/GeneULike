from django.urls import path
from geneulike.series import views


app_name = "series"
urlpatterns = [
    path('create/<int:study_id>', views.serie_create_form, name="serie_create"),
]
