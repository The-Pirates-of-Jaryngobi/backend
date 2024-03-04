from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),  # https://wikidocs.net/70649
]
