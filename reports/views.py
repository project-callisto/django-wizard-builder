from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    return HttpResponse('<html><head><title>Callisto</title></head></html>')