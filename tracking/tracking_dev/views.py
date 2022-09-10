from django.shortcuts import render
from django.http import HttpResponse


# This view provides main page.
def index(request):
    return render(request, 'include/main_page.html')
