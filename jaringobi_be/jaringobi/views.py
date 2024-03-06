from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .lambda_function import lambda_handler

import json
from .logger import *
set_file_logger()

# https://wikidocs.net/70649
def home(request):
    return HttpResponse("최저가 유튜버 레시피는?")


@api_view(['POST'])
def search(request):
    menu_name = json.loads(request.body)['menu_name']
    return Response(lambda_handler(menu_name))