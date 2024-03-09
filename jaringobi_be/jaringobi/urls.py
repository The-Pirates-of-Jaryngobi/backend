from django.urls import path, include

from .views import *

urlpatterns = [
    path('', home),  # https://wikidocs.net/70649
    path('search/', search),
    # path('api/', include('rest_framework.urls')),
]
