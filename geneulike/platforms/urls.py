from django.urls import path, re_path
from geneulike.platforms import views

app_name = "platforms"
urlpatterns = [
    re_path(r'^autocomplete/$', views.PlatformAutocomplete.as_view(), name="platform-autocomplete"),
]
