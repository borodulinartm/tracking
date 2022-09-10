from django.db.models import Q
from django.utils.timezone import now
from django.contrib import auth, messages
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import *


# This view provides a main page.
def index(request):
    return render(request, 'include/main_page.html')


# This view provides a list of the projects (displayed by the table)
def get_list_projects(request):
    raw_data = Project.objects.raw(
        raw_query="SELECT * FROM tracking_dev_project"
    )

    head = ["Номер", "Название", "Описание"]

    return render(request, 'include/content/project_list.html', {
        'title_page': 'Картотека проектов',
        'head': head,
        'table': raw_data
    })


# This is the view, which provide description about this project
def project_description(request, project_id):
    raw_data = Project.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_project WHERE project_id = {project_id}"
    )

    head = ["Номер", "Название", "Описание"]
    return render(request, "include/description/project.html", {
        'title_page': 'Сведения о проекте',
        'head': head,
        'table': raw_data
    })
