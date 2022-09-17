from django.db.models import Q
from django.utils.timezone import now
from django.contrib import auth, messages
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import *


# This view provides a main page.
def index(request):
    return render(request, 'include/main_page.html', {
        'title_page': 'Привет, мир',
        'show_list_group': 0
    })


# This view provides a list of the projects (displayed by the table)
def get_list_projects(request):
    raw_data = Project.objects.raw(
        raw_query="SELECT * FROM tracking_dev_project"
    )

    return render(request, 'include/list.html', {
        'title_page': 'Выберите проект для его просмотра или удаления',
        'show_list_group': 1,
        'data_group': raw_data,
        'what_open': 1
    })


# This is the view, which provide description about this project
def project_description(request, project_id):
    raw_data = Project.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_project WHERE project_id = {project_id}"
    )

    data = Project.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_project"
    )

    head = ["Номер", "Код", "Название", "Описание", "Дата создания"]
    return render(request, "include/description/project.html", {
        'title_page': 'Сведения о проекте',
        'head': head,
        'table': raw_data,
        'show_list_group': 1,
        'data_group': data,
        'what_open': 1
    })


# This view provides list of the states
def get_state_list(request):
    raw_data = State.objects.raw(
        raw_query="SELECT * FROM tracking_dev_state"
    )

    return render(request, "include/list.html", {
        'title_page': "Выберите состояние задачи для его просмотра или удаления",
        'show_list_group': 1,
        'data_group': raw_data,
        'what_open': 2
    })


def state_description(request, state_id):
    raw_data = State.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_state WHERE state_id = {state_id}"
    )

    data = State.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_state"
    )

    head = ["Номер", "Код", "Название", "Описание", "Дата создания"]
    return render(request, "include/description/state.html", {
        'title_page': 'Сведения о состоянии задачи',
        'head': head,
        'table': raw_data,
        'show_list_group': 1,
        'data_group': data,
        'what_open': 2
    })


# This view provides a list of the task priority table
def get_priority_list(request):
    raw_data = Priority.objects.raw(
        raw_query="SELECT * FROM tracking_dev_priority"
    )

    return render(request, "include/list.html", {
        'title_page': "Выберите приоритет задачи для его просмотра или удаления",
        'show_list_group': 1,
        'data_group': raw_data,
        'what_open': 3
    })


# This view provides a description of the file
def priority_description(request, priority_id):
    raw_data = Priority.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_priority WHERE priority_id = {priority_id}"
    )

    data = Priority.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_priority"
    )

    head = ["Номер", "Код", "Название", "Описание", "Дата создания"]
    return render(request, "include/description/priority.html", {
        'title_page': 'Сведение о приоритете задачи',
        'head': head,
        'table': raw_data,
        'show_list_group': 1,
        'data_group': data,
        'what_open': 3
    })


# This view provides a list of the types tasks (like new feature, test, task or bug)
def type_task_list(request):
    raw_data = TypeTask.objects.raw(
        raw_query="SELECT * FROM tracking_dev_typetask"
    )

    return render(request, "include/list.html", {
        'title_page': 'Выберите тип задачи для его просмотра или удаления',
        'show_list_group': 1,
        'data_group': raw_data,
        'what_open': 4
    })


# This view provides a description of the type task
def type_task_description(request, type_id):
    # Select the task by id
    raw_data = TypeTask.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_typetask WHERE type_id = {type_id}"
    )

    # Select all tasks
    data = TypeTask.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_typetask"
    )

    head = ["Номер", "Код", "Название", "Описание", "Дата создания"]
    return render(request, "include/description/type.html", {
        'title_page': 'Сведения о типе задачи',
        'head': head,
        'table': raw_data,
        'show_list_group': 1,
        'data_group': data,
        'what_open': 4
    })
