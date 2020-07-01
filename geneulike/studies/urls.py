from django.urls import path
from geneulike.studies import views

app_name = "studies"
urlpatterns = [
    path('create/', views.study_create_form, name="study_create"),
]
