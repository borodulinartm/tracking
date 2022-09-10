from django.shortcuts import render
from django.http import HttpResponse


# This view provides main page.
def index(request):
    return HttpResponse("Hello world. You're from the index function")
