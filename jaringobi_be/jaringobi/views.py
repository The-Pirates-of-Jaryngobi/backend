from django.shortcuts import render
from django.http import HttpResponse

# https://wikidocs.net/70649
def home(request):
    return HttpResponse("최저가 유튜버 레시피는?")

