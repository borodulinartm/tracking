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


# This employee provides an employee list
def employee_list(request):
    raw_data = Employee.objects.raw(
        raw_query="select au.first_name, au.last_name, tde.employee_id, tde.post, tde.description, tde.date_create "
                  "from tracking_dev_employee tde join auth_user au on au.id = tde.user_id;"
    )

    return render(request, "include/list.html", {
        'title_page': 'Выберите сотрудника для его просмотра или удаления',
        'show_list_group': 1,
        'data_group': raw_data,
        'what_open': 5
    })


# This employee provides a description of the employee
def employee_description(request, employee_id):
    raw_data = Employee.objects.raw(
        raw_query=f"select * from tracking_dev_employee tde join auth_user au on au.id = tde.user_id "
                  f"where employee_id = {employee_id};"
    )

    data = Employee.objects.raw(
        raw_query="select au.first_name, au.last_name, tde.employee_id, tde.post, tde.description, tde.date_create "
                  "from tracking_dev_employee tde join auth_user au on au.id = tde.user_id;"
    )

    head = ["Номер", "Должность", "Описание", "Дата"]
    return render(request, "include/description/employee.html", {
        'title_page': 'Сведения о сотруднике',
        'head': head,
        'table': raw_data,
        'show_list_group': 1,
        'data_group': data,
        'what_open': 5
    })


# This view provides a list of the tasks
def task_list(request):
    raw_data = Task.objects.raw(
        raw_query="SELECT * FROM tracking_dev_task"
    )

    return render(request, "include/list.html", {
        'title_page': "Выберите задачу для его просмотра или удаления",
        'show_list_group': 1,
        'data_group': raw_data,
        'what_open': 6
    })


def task_description(request, task_id):
    raw_data = Task.objects.raw(
        raw_query=f"select tdt.task_id, tdt.code, tdt.name, tdt.description, au.first_name  as init_name,"
                  f"au.last_name as init_surname, au2.last_name as resp_surname,"
                    f"au2.first_name  as resp_name, tds.name as state_name, tdp.name as project_name, "
                    f"tdp2.name as priority_name, tdt2.name as type_task_name from tracking_dev_task tdt  "
                    f"join tracking_dev_employee tde on tde.employee_id = tdt.initiator_id join tracking_dev_state tds "
                    f"on tds.state_id = tdt.state_id join tracking_dev_project tdp on tdp.project_id = tdt.project_id "
                    f"join tracking_dev_priority tdp2 on tdp2.priority_id = tdt.priority_id join tracking_dev_employee "
                    f"tde2 on tde2.employee_id = tdt.responsible_id join tracking_dev_typetask tdt2 "
                    f"on tdt2.type_id = tdt.type_id join auth_user au on au.id = tde.user_id "
                    f"join auth_user au2 on au2.id = tde2.user_id WHERE tdt.task_id = {task_id};"
    )

    data = Task.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_task"
    )

    head = ["ID", "Код", "Название", "Описание", "Инициатор", "Ответственный", "Состояние", "Проект", "Приоритет", "Тип"]
    return render(request, "include/description/task.html", {
        'title_page': 'Сведения о задаче',
        'head': head,
        'table': raw_data,
        'show_list_group': 1,
        'data_group': data,
        'what_open': 6
    })
