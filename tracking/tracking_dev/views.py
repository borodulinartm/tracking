from django.db.models import Q
from django.utils.timezone import now
from django.contrib import auth, messages
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db import connection

from .models import *
from .forms import *

import random


# Данная функция проверяет, что текущий пользователь действительно относится к этому проекту
def is_user_in_this_project(request, project_id):
    query = f"select 1 as project_id, COUNT(*) from tracking_dev_employee_projects tdep " \
            f"join tracking_dev_employee tde ON tdep.employee_id = tde.employee_id " \
            f"join auth_user au on au.id = tde.user_id " \
            f"where tdep.project_id = {project_id} and au.id = {request.user.id}"

    raw_data = Project.objects.raw(raw_query=query)

    print(query)

    for data in raw_data:
        return data.count > 0


# This view provides a main page.
def index(request):
    if request.user.is_authenticated:
        raw_data = Project.objects.raw(
            raw_query=f"select tdp.project_id, tdp.\"name\", tdp.description, tdp.date_create, tdp.code, 1 as project_exists "
                      f"from tracking_dev_employee_projects tdep "
                      f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                      f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                      f"where tde.user_id = {request.user.id};"
        )
    else:
        raw_data = []

    return render(request, 'include/main_page.html', {
        'title_page': 'Привет, мир',
        'show_list_group': 0,
        'show_choose_project': 1,
        'list_projects': raw_data
    })


# This view allows admin show and create tasks
def show_extra_functions(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    raw_data = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/list_data/project_list_functions.html", {
        'show_list_group': 0,
        'show_choose_project': 1,
        'is_project_zone': 1,
        'list_projects': raw_data,
        'project_id': project_id
    })


# This view allows admin show tasks for current project
def show_list_tasks_for_project(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not is_user_in_this_project(request, project_id):
        return HttpResponseForbidden()

    raw_data = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/list_data/tasks_list.html", {
        'title_page': 'Выберите задачу для просмотра',
        'show_list_group': 0,
        'show_choose_project': 1,
        'is_project_zone': 1,
        'list_projects': raw_data,

        'is_admin': request.user.is_staff,
        'project_id': project_id,
    })


# This view provides a list of the projects (displayed by the table)
def get_list_projects(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    raw_data = Project.objects.raw(
        raw_query=f"select tdp.project_id, tdp.\"name\", tdp.description, tdp.date_create, tdp.code, 1 as project_exists "
                  f"from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, 'include/list_data/project_list.html', {
        'title_page': 'Выберите проект для его просмотра или удаления',
        'show_list_group': 0,
        'show_choose_project': 1,
        'list_projects': raw_data,
        'data_group': raw_data,
        'value_in_the_search_form': ''
    })


# This is the view, which provide description about this project
def project_description(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    raw_data = Project.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_project WHERE project_id = {project_id} and is_activate=True"
    )

    participants = Project.objects.raw(
        raw_query=f"select au.first_name, au.last_name, tde.post,  tdep.project_id, tdep.employee_id , au.email "
                  f"from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tde.employee_id = tdep.employee_id "
                  f"join auth_user au on au.id = tde.user_id "
                  f"where project_id = {project_id} and tdep.is_activate=True;"
    )

    count_tasks = Task.objects.raw(
        raw_query=f"select * from tracking_dev_task tdt where tdt.project_id = {project_id} and is_activate=True"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select tdp.project_id, tdp.code, tdp.date_create, tdp.description from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    head = ["Номер", "Код", "Название", "Описание", "Дата создания"]
    return render(request, "include/description/project.html", {
        'title_page': 'Сведения о проекте',
        'head': head,
        'table': raw_data,
        'show_list_group': 1,
        'count_tasks': len(list(count_tasks)),
        'data_group': all_projects,
        'participants': participants,
        'what_open': 1,
        'show_choose_project': 1,
        'list_projects': all_projects
    })


def get_sprint_list_for_project(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    raw_data = Sprint.objects.raw(
        raw_query=f"select * from tracking_dev_sprint tds where tds.project_id = {project_id} and tds.is_activate ;"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, 'include/list_data/sprint_list.html', {
        'title_page': 'Выберите спринт для его просмотра или удаления',
        'show_list_group': 0,
        'show_choose_project': 1,
        'list_sprint': raw_data,
        'data_group': all_projects,
        'list_projects': all_projects,
        'is_project_zone': 1,
        'project_id': project_id,
        'value_in_the_search_form': ''
    })


def sprint_description(request, project_id, sprint_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    sprint_desc = Sprint.objects.raw(
        raw_query=f"select * from tracking_dev_sprint tds "
                  f"where tds.project_id = {project_id} and tds.sprint_id = {sprint_id} and tds.is_activate ;"
    )

    data = Sprint.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_sprint tds where is_activate=True and tds.project_id = {project_id}"
    )

    list_tasks = Task.objects.raw(
        raw_query=f"select * from tracking_dev_sprint_task tdst "
                  f"join tracking_dev_task tdt on tdst.task_id = tdt.task_id where tdst.sprint_id = {sprint_id}"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    head = ["Номер", "Код", "Название", "Описание", "Дата создания", "Дата начала", "Дата завершения"]

    return render(request, "include/description/sprint.html", {
        'title_page': 'Сведения о спринте',
        'head': head,
        'table': sprint_desc,
        'show_list_group': 1,
        'data_group': data,
        'what_open': 7,
        'is_project_zone': 1,
        'tasks': list_tasks,
        'project_id': project_id,
        'sprint_id': sprint_id,
        'show_choose_project': 1,
        'list_projects': all_projects
    })


# This view provides list of the states
def get_state_list(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    # The settings are disable for the developer
    if not request.user.is_staff:
        return HttpResponseForbidden()

    raw_data = State.objects.raw(
        raw_query="SELECT *, 1 as state_exists FROM tracking_dev_state where is_activate=True"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/list_data/state_list.html", {
        'title_page': "Выберите состояние задачи для его просмотра или удаления",
        'show_list_group': 0,
        'data_group': raw_data,
        'show_choose_project': 1,
        'list_projects': all_projects
    })


def state_description(request, state_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    raw_data = State.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_state WHERE state_id = {state_id} and is_activate=True"
    )

    data = State.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_state where is_activate=True"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    tasks_with_current_state_id = Task.objects.filter(state_id=state_id).count()

    head = ["Номер", "Код", "Название", "Описание", "Дата создания"]
    return render(request, "include/description/state.html", {
        'title_page': 'Сведения о состоянии задачи',
        'head': head,
        'table': raw_data,
        'show_list_group': 1,
        'data_group': data,
        'what_open': 2,
        'count_tasks': tasks_with_current_state_id,
        'show_choose_project': 1,
        'list_projects': all_projects
    })


# This view provides a list of the task priority table
def get_priority_list(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    raw_data = Priority.objects.raw(
        raw_query="SELECT *, 1 as code_exists FROM tracking_dev_priority where is_activate=True"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/list_data/priority_list.html", {
        'title_page': "Выберите приоритет задачи для его просмотра или удаления",
        'show_list_group': 0,
        'data_group': raw_data,
        'show_choose_project': 1,
        'list_projects': all_projects
    })


# This view provides a description of the file
def priority_description(request, priority_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    raw_data = Priority.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_priority WHERE priority_id = {priority_id} and is_activate=True"
    )

    data = Priority.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_priority where is_activate=True"
    )

    count_tasks = Task.objects.raw(
        raw_query=f"select * from tracking_dev_task tdt where tdt.priority_id = {priority_id} and is_activate=True"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    head = ["Номер", "Код", "Название", "Описание", "Дата создания"]
    return render(request, "include/description/priority.html", {
        'title_page': 'Сведение о приоритете задачи',
        'head': head,
        'table': raw_data,
        'show_list_group': 1,
        'count_tasks': len(list(count_tasks)),
        'data_group': data,
        'show_choose_project': 1,
        'what_open': 3,
        'list_projects': all_projects
    })


# This view provides a list of the types tasks (like new feature, test, task or bug)
def type_task_list(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    raw_data = TypeTask.objects.raw(
        raw_query="SELECT *, 1 as code_exists FROM tracking_dev_typetask where is_activate=True"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/list_data/type_task_list.html", {
        'title_page': 'Выберите тип задачи для его просмотра или удаления',
        'show_list_group': 0,
        'data_group': raw_data,
        'show_choose_project': 1,
        'list_projects': all_projects
    })


# This view provides a description of the type task
def type_task_description(request, type_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    # Select the task by ID
    raw_data = TypeTask.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_typetask WHERE type_id = {type_id} and is_activate=True"
    )

    # Select all tasks
    data = TypeTask.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_typetask"
    )

    count_tasks = Task.objects.raw(
        raw_query=f"select * from tracking_dev_task tdt where tdt.type_id = {type_id} and is_activate=True"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/description/type.html", {
        'title_page': 'Сведения о типе задачи',
        'table': raw_data,
        'show_list_group': 1,
        'count_tasks': len(list(count_tasks)),
        'data_group': data,
        'what_open': 4,
        'show_choose_project': 1,
        'list_projects': all_projects
    })


# This employee provides an employee list
def employee_list(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    raw_data = Employee.objects.raw(
        raw_query="select au.first_name, au.last_name, tde.employee_id, tde.post, tde.description, tde.date_create, "
                  "1 as name_exists "
                  "from tracking_dev_employee tde join auth_user au on au.id = tde.user_id where tde.is_activate=True;"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/list_data/employee_list.html", {
        'title_page': 'Выберите сотрудника для его просмотра или удаления',
        'show_list_group': 0,
        'data_group': raw_data,
        'show_choose_project': 1,
        'list_projects': all_projects
    })


# This employee provides a description of the employee
def employee_description(request, employee_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    raw_data = Employee.objects.raw(
        raw_query=f"select * from tracking_dev_employee tde join auth_user au on au.id = tde.user_id "
                  f"where employee_id = {employee_id} and is_activate=True;"
    )

    data = Employee.objects.raw(
        raw_query="select au.first_name, au.last_name, tde.employee_id, tde.post, tde.description, tde.date_create "
                  "from tracking_dev_employee tde join auth_user au on au.id = tde.user_id where tde.is_activate=True;"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/description/employee.html", {
        'title_page': 'Сведения о сотруднике',
        'table': raw_data,
        'show_list_group': 1,
        'data_group': data,
        'show_choose_project': 1,
        'what_open': 5,
        'list_projects': all_projects
    })


def task_description(request, project_id, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not is_user_in_this_project(request, project_id):
        return HttpResponseForbidden()

    raw_data = Task.objects.raw(
        raw_query=f"select tdt.task_id, tdt.code, tdt.name, tdt.description, tds.percentage, au.first_name  as init_name, "
                  f"au.last_name as init_surname, au2.last_name as resp_surname, "
                  f"au2.first_name  as resp_name, tds.name as state_name, tdp.name as project_name, "
                  f"tdp2.name as priority_name, tdt2.name as type_task_name, au3.first_name as manager_name, "
                  f"au3.last_name as manager_last_name "
                  f"from tracking_dev_task tdt  "
                  f"join tracking_dev_employee tde on tde.employee_id = tdt.initiator_id  "
                  f"join tracking_dev_state tds "
                  f"on tds.state_id = tdt.state_id join tracking_dev_project tdp on tdp.project_id = tdt.project_id "
                  f"join tracking_dev_employee tde3 on tde3.employee_id = tdt.manager_id "
                  f"join auth_user au3 on au3.id = tde3.user_id  "
                  f"join tracking_dev_priority tdp2 on tdp2.priority_id = tdt.priority_id join tracking_dev_employee "
                  f"tde2 on tde2.employee_id = tdt.responsible_id join tracking_dev_typetask tdt2 "
                  f"on tdt2.type_id = tdt.type_id join auth_user au on au.id = tde.user_id "
                  f"join auth_user au2 on au2.id = tde2.user_id "
                  f"where tdt.is_activate=true and tdt.task_id = {task_id};"
    )

    list_of_subtasks = SubTasks.objects.raw(
        raw_query=f"select 1 as sub_task_id, tdt.task_id, tdt.code, tdt.\"name\", tdt.description, "
                  f"tdt.date_change from tracking_dev_subtasks tds "
                  f"join tracking_dev_task tdt on tds.task_id = tdt.task_id "
                  f"join tracking_dev_state tds2 on tds2.state_id = tdt.state_id "
                  f"where tds.reference_task_id = {task_id} and tds2.\"isClosed\" = false "
                  f"and tdt.is_activate=True"
    )

    data = Task.objects.raw(
        raw_query=f"select * from tracking_dev_task tdt "
                  f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                  f"where tdt.project_id = {project_id} and tdt.is_activate and "
                  f"tds.\"isClosed\" = false"
    )

    list_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    employee_id_list = Employee.objects.filter(user_id=request.user.id)
    employee_id = 0

    for current_employee in employee_id_list:
        employee_id = current_employee.employee_id

    # Add the check if the current user has voted to the task.
    user_voted = Employee.objects.raw(
        raw_query=f"select * from tracking_dev_task_employee tdte "
                  f"where tdte.employee_id = {employee_id} and tdte.task_id = {task_id}"
    )

    count_votes = Employee.objects.raw(
        raw_query=f"select tdte.id, tdte.employee_id, au.first_name, au.last_name, "
                  f"tde.post from tracking_dev_task_employee tdte "
                  f"join tracking_dev_employee tde on tde.employee_id = tdte.employee_id "
                  f"join auth_user au on au.id = tde.user_id  "
                  f"where tdte.task_id = {task_id}"
    )

    # The user capacity
    laboriousness = Laboriousness.objects.raw(
        raw_query=f"select 1 as laboriousness_id, tdl.capacity_plan, tdl.capacity_fact, tdl.task_id, au.first_name, "
                  f"au.last_name from tracking_dev_laboriousness tdl "
                  f"join tracking_dev_employee tde on tdl.employee_id = tde.employee_id "
                  f"join auth_user au on au.id = tde.user_id "
                  f"where tdl.task_id = {task_id}"
    )

    return render(request, "include/description/task.html", {
        'title_page': 'Сведения о задаче',
        'table': raw_data,
        'show_list_group': 1,
        'data_group': data,
        'project_id': project_id,
        'is_project_zone': 1,
        'show_choose_project': 0,
        'count_subtasks': len(list(list_of_subtasks)),
        'is_current_user_voted': len(list(user_voted)) > 0,
        'count_votes': len(list(count_votes)),
        'votes': count_votes,
        'subtasks': list_of_subtasks,
        'laboriousness': laboriousness,
        'list_projects': list_projects,
        'is_admin': request.user.is_staff,
        'task_id': task_id,
        'what_open': 6
    })


# This method allows user get the capacity and set to the table
def form_capacity_table(request, project_id, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not is_user_in_this_project(request, project_id):
        return HttpResponseForbidden()

    if request.method == "GET":
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            # The user capacity
            laboriousness = Laboriousness.objects.raw(
                raw_query=f"select tdl.laboriousness_id, tdl.employee_id, tdl.capacity_plan, tdl.capacity_fact, tdl.task_id, au.first_name, "
                          f"au.last_name from tracking_dev_laboriousness tdl "
                          f"join tracking_dev_employee tde on tdl.employee_id = tde.employee_id "
                          f"join auth_user au on au.id = tde.user_id "
                          f"where tdl.task_id = {task_id}"
            )

            data = []
            for element in laboriousness:
                item = {
                    "laboriousness_id": element.laboriousness_id,
                    "employee_id": element.employee_id,
                    "task_id": element.task_id,
                    "capacity_plan": element.capacity_plan,
                    "capacity_fact": element.capacity_fact,
                    "user_name": element.first_name + " " + element.last_name
                }

                data.append(item)

            return JsonResponse({'data': data})
    return JsonResponse({'data': []})


# This view allows you to remove project. But it cannot remove if the tasks linked to project exists.
def project_remove(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    Project.objects.filter(project_id=project_id).update(is_activate=False)
    return redirect(reverse('projects'))


# This view allows user remove sprint from the task
def sprint_remove(request, project_id, sprint_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    Sprint.objects.filter(sprint_id=sprint_id).update(is_activate=False)
    return redirect(reverse('sprints', kwargs={'project_id': project_id}))


# This view allows user remove task from sprint
def remove_task_from_sprint(request, project_id, sprint_id, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    with connection.cursor() as cursor:
        cursor.execute(f"delete from tracking_dev_sprint_task tdst where tdst.sprint_id = {sprint_id} "
                       f"and tdst.task_id = {task_id}")

    return redirect(reverse('sprint_description', kwargs={'project_id': project_id, 'sprint_id': sprint_id}))


# This view allows you remove the task
def task_remove(request, project_id, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    Task.objects.filter(task_id=task_id).update(is_activate=False)
    return redirect(reverse('tasks_for_project', kwargs={"project_id": project_id}))


# This view allows you remove the priority
def priority_remove(request, priority_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    Priority.objects.filter(priority_id=priority_id).update(is_activate=False)
    return redirect(reverse('priorities'))


# This view allows user remove the state from the project
# But in the project all tasks with the current state_id must be wiped out from the system due to errors.
def state_remove(request, state_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    State.objects.filter(state_id=state_id).update(is_activate=False)
    return redirect(reverse('states'))


# This view allows you to remove the employee
def employee_remove(request, employee_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    Employee.objects.filter(employee_id=employee_id).update(is_activate=False)
    return redirect(reverse('employees'))


# This view allows you to remove the type of task
def type_remove(request, type_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    TypeTask.objects.filter(type_id=type_id).update(is_activate=False)
    return redirect(reverse('types'))


# This view provides a list of the collaborators for current project.
def get_list_collobarators_to_project(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    participants = Project.objects.raw(
        raw_query=f"select au.first_name, au.last_name, au.id, tde.post, tdep.project_id, tdep.employee_id , au.email "
                  f"from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tde.employee_id = tdep.employee_id "
                  f"join auth_user au on au.id = tde.user_id "
                  f"where project_id = {project_id} and tdep.is_activate=True;"
    )

    all_projects = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/description/collobarators.html", {
        'title_page': 'Участники проекта',
        'table': participants,
        'show_list_group': 0,
        'project_id': project_id,
        'show_choose_project': 1,
        'is_project_zone': 1,
        'list_projects': all_projects,
        'is_admin_zone': request.user.is_staff,
        'id': request.user.id
    })


# This view allows admin remove the user from current project
def remove_user_from_current_project(request, project_id, employee_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    # Because the query contains UPDATE, we need use connection.cursor() instead of objects.raw
    with connection.cursor() as cursor:
        cursor.execute(f"delete from tracking_dev_employee_projects where "
                       f"project_id={project_id} and employee_id={employee_id}")

    # Redirect to the website with projects
    return redirect(reverse("collabs", kwargs={'project_id': project_id}))


# This method remove the current value from the table of capacity.
def remove_row_from_capacity_table(request, project_id, task_id, employee_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    with connection.cursor() as cursor:
        cursor.execute(f"delete from tracking_dev_laboriousness tdl "
                       f"where tdl.employee_id = {employee_id} and tdl.task_id = {task_id};")

    return redirect(reverse('task_description', kwargs={'project_id': project_id, 'task_id': task_id}))


# This view allows admin remove all users from this project
def remove_all_users_from_current_project(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    # We should delete entirely from the database
    with connection.cursor() as cursor:
        cursor.execute(f"update tracking_dev_employee_projects tdep "
                       f"set is_activate = false "
                       f"from tracking_dev_employee tde "
                       f"where tde.employee_id = tdep.employee_id and tde.user_id != {request.user.id} "
                       f"and tdep.project_id = {project_id}")

    # Redirect to the website with project
    return redirect(reverse('collabs', kwargs={"project_id": project_id}))


# This view provides a creation form of the project
def create_project(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    # Create something can only manager (or another admin)
    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == "POST":
        creation_form = CreateProjectForm(data=request.POST)

        # If the form is valid, you should add the user to this project.
        if creation_form.is_valid():
            creation_form.save()

            # Auto add manager to table
            code = creation_form.cleaned_data['code']

            new_project = Project.objects.raw(
                raw_query=f"SELECT * FROM tracking_dev_project WHERE code='{code}'"
            )
            list_employees = Employee.objects.raw(
                raw_query=f"SELECT * FROM tracking_dev_employee WHERE user_id={request.user.id}"
            )

            project_id = 0
            employee_id = 0

            for current_project in new_project:
                project_id = current_project.project_id

            for current_employee in list_employees:
                employee_id = current_employee.employee_id

            with connection.cursor() as cursor:
                cursor.execute(f"insert into tracking_dev_employee_projects(employee_id, project_id, is_activate) "
                               f"values ({employee_id}, {project_id}, True)")

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            messages.error(request, "Ошибка валидации формы")
    else:
        creation_form = CreateProjectForm()

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма создания нового проекта',
        'form': creation_form,
        'text_button': 'Создать проект',
        'show_choose_project': 0,
    })


# These methods provide edit project
def edit_project(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    instance = get_object_or_404(Project, project_id=project_id)
    form = CreateProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    return render(request, 'include/base_form.html', {
        'form': form,
        'title_page': 'Форма редактироваиня проекта',
        'text_button': 'Сохранить изменения',
        'show_choose_project': 0,
    })


def create_priority(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == "POST":
        creation_form = CreatePriorityForm(data=request.POST)

        if creation_form.is_valid():
            creation_form.save()

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        creation_form = CreateProjectForm()

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма создания нового приоритета',
        'form': creation_form,
        'text_button': 'Создать приоритет',
        'show_choose_project': 0,
    })


# This view provides create sprint form
def create_sprint(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    if request.method == "POST":
        creation_form = CreateSprintForm(data=request.POST)

        if creation_form.is_valid():
            code = creation_form.cleaned_data['code']
            name = creation_form.cleaned_data['name']
            description = creation_form.cleaned_data['description']
            date_start = creation_form.cleaned_data['date_start']
            date_end = creation_form.cleaned_data['date_end']

            SprintData = Sprint(code=code, name=name, description=description, project_id=project_id,
                                date_start=date_start, date_end=date_end)
            SprintData.save()

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        creation_form = CreateSprintForm()

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма создания нового спринта',
        'form': creation_form,
        'text_button': 'Создать спринт',
        'show_choose_project': 0
    })


# This view provides edit form of the sprint
def edit_sprint(request, project_id, sprint_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    instance = get_object_or_404(Sprint, sprint_id=sprint_id)
    form = CreateSprintForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма редактирования спринта',
        'form': form,
        'text_button': 'Применить изменения',
        'show_choose_project': 0
    })


def edit_priority(request, priority_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    instance = get_object_or_404(Priority, priority_id=priority_id)
    form = CreatePriorityForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма редактирования приоритета',
        'form': form,
        'text_button': 'Применить изменения',
        'show_choose_project': 0,
    })


# This function provides a creation instance of the laboriousness
def create_laboriousness(request, project_id, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    if request.method == "POST":
        creation_form = CreateLaboriousnessForm(data=request.POST)
        if creation_form.is_valid():
            employee = str(creation_form.cleaned_data['employee'])

            capacity_plan = creation_form.cleaned_data['capacity_plan']
            capacity_fact = creation_form.cleaned_data['capacity_fact']

            employee_name, employee_surname = employee.split()
            s = User.objects.raw(
                raw_query=f"select 1 as id, tde.employee_id  from auth_user au join tracking_dev_employee "
                          f"tde on au.id = tde.user_id "
                          f"where au.first_name = '{employee_name}' and au.last_name = '{employee_surname}'"
            )

            employee_id = 0
            for data in s:
                employee_id = data.employee_id

            # We need check if the user exists in the task
            is_user_exists = Task.objects.raw(
                raw_query=f"select * from tracking_dev_task tdt where (tdt.initiator_id = {employee_id} or "
                          f"tdt.responsible_id = {employee_id} or tdt.manager_id = {employee_id}) and tdt.task_id = {task_id}"
            )

            list_data = Laboriousness.objects.raw(
                raw_query=f"select 1 as laboriousness_id, * from tracking_dev_laboriousness tdl "
                          f"where tdl.employee_id = {employee_id} and tdl.task_id = {task_id}"
            )

            # This condition are necessary, because we can have the similar record in the table.
            if len(list(list_data)) == 0 and len(list(is_user_exists)) > 0:
                if capacity_fact is None:
                    capacity_fact = capacity_plan
                record = Laboriousness(employee_id=employee_id, capacity_plan=capacity_plan,
                                       capacity_fact=capacity_fact, task_id=task_id)
                record.save()

                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
            else:
                if len(list(list_data)) > 0:
                    messages.error(request, "Трудоёмкость для данного пользователя уже "
                                            "имеется в системе. Пожалуйста, выберите другого пользователя или отредактируйте"
                                            " запись для данного")
                elif len(list(is_user_exists)) == 0:
                    messages.error(request, "Данный сотрудник ничего не имеет общего с данной задачей")
        else:
            messages.error(request, "Произошла ошибка при вводе данных. Убедитесь, что информация введена верно")
    else:
        creation_form = CreateLaboriousnessForm()

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма добавления записи к трудоёмкости задачи',
        'form': creation_form,
        'text_button': 'Добавить данные',
        'show_choose_project': 0
    })


# This function provides edit the laboriousness.
def edit_laboriousness(request, project_id, task_id, laboriousness_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    instance = get_object_or_404(Laboriousness, laboriousness_id=laboriousness_id)

    form = CreateLaboriousnessForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма редактирования записи трудоёмкости задачи',
        'form': form,
        'text_button': 'Применить изменения',
        'show_choose_project': 0,
    })


# This view allows admin create states for project
def create_state(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == "POST":
        creation_form = CreateStateForm(data=request.POST)

        # If the form is valid, then we need to check if the isClosed states exists.
        if creation_form.is_valid():
            name = creation_form.cleaned_data['name']
            description = creation_form.cleaned_data['description']
            percentage = creation_form.cleaned_data['percentage']
            code = creation_form.cleaned_data['code']
            is_ticked_checkbox = creation_form.cleaned_data['isClosed']

            next = request.POST.get('next', '/')

            if is_ticked_checkbox:
                count_closed_states = State.objects.filter(isClosed=True).count()

                if count_closed_states == 0:
                    my_state = State(name=name, code=code, description=description, percentage=100,
                                     is_ticked_checkbox=is_ticked_checkbox)
                    my_state.save()

                    return HttpResponseRedirect(next)
                else:
                    messages.error(request, "Состояние закрытой задачи уже существует в системе")
            else:
                # Если % выполнения задачи > 100, то выдаём ошибку, так как процент не может быть больше 99
                # для незакрытого состояния
                if percentage >= 100:
                    messages.error(request,
                                   "Процент выполнения задачи не может превышать 99 для не закрытого состояния задачи")
                else:
                    creation_form.save()
                    return HttpResponseRedirect(next)
        else:
            messages.error(request, "Произошла ошибка при вводе данных. Убедитесь, что информация введена верно")
    else:
        creation_form = CreateStateForm()

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма создания нового состояния задачи',
        'form': creation_form,
        'text_button': 'Создать состояние',
        'show_create_project': 0
    })


# This view allows to edit priority
def edit_states(request, state_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    instance = get_object_or_404(State, state_id=state_id)
    form = CreateStateForm(request.POST or None, instance=instance)

    if form.is_valid():
        percentage = form.cleaned_data['percentage']
        is_checkbox_ticked = form.cleaned_data['isClosed']

        next = request.POST.get('next', '/')

        # The condition of the count closed tasks can be if the checkbox has ticked.
        if is_checkbox_ticked:
            count_another_closed_tasks = State.objects.filter(Q(isClosed=True) & ~Q(state_id=state_id)).count()

            if count_another_closed_tasks == 0:
                form.save()
                return HttpResponseRedirect(next)
            else:
                messages.error(request,
                               "В базе данных уже имеется состояние, при котором задача может считаться закрытой")
        else:
            if percentage >= 100:
                messages.error(request,
                               "Процент выполнения задачи не может превышать 99 для не закрытого состояния задачи")
            else:
                form.save()
                return HttpResponseRedirect(next)

    return render(request, "include/base_form.html", {
        'title_page': 'Форма рредактирования текущего состояния',
        'form': form,
        'text_button': 'Применить изменения',
        'show_choose_project': 0
    })


def create_type_task(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == "POST":
        creation_form = CreateTypeTaskForm(data=request.POST)
        if creation_form.is_valid():
            creation_form.save()

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        creation_form = CreateTypeTaskForm()

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма создания нового типа задачи',
        'form': creation_form,
        'text_button': 'Создать тип задачи',
        'show_choose_project': 0,
    })


def edit_type_task(request, type_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not request.user.is_staff:
        return HttpResponseForbidden()

    instance = get_object_or_404(TypeTask, type_id=type_id)
    form = CreateTypeTaskForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма редактирования типа задачи',
        'form': form,
        'text_button': 'Сохранить изменения',
        'show_choose_project': 0,
    })


# This view provides task creation form
def create_task(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    raw_data = Project.objects.filter(project_id=project_id)

    arr = None
    for data in raw_data:
        arr = data

    # This query provides an employee creation form
    employee = Employee.objects.filter(user_id=request.user.id)
    employee_arr = None
    for data in employee:
        employee_arr = data

    if request.method == "POST":
        creation_form = CreateTaskForm(data=request.POST)
        if creation_form.is_valid():
            code = creation_form.cleaned_data['code']
            name = creation_form.cleaned_data['name']
            description = creation_form.cleaned_data['description']
            responsible = creation_form.cleaned_data['responsible']
            initiator = creation_form.cleaned_data['initiator']
            state = creation_form.cleaned_data['state']
            priority = creation_form.cleaned_data['priority']
            type_task = creation_form.cleaned_data['type']
            date_deadline = creation_form.cleaned_data['date_deadline']

            task = Task(code=code, name=name, description=description, responsible=responsible, initiator=initiator,
                        state=state, priority=priority, type=type_task, date_deadline=date_deadline, project=arr,
                        manager=employee_arr)
            task.save()

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        creation_form = CreateTaskForm()

        # Use a many-to-many query
        creation_form.fields['responsible'].queryset = Employee.objects.filter(projects=project_id)
        creation_form.fields['initiator'].queryset = Employee.objects.filter(projects=project_id)

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма создания новой задачи',
        'form': creation_form,
        'text_button': 'Создать задачу',
        'show_choose_project': 0,
        'project_id': project_id,
    })


# This view provides creation form of the subtasks
def create_subtask_form(request, project_id, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    raw_data = Project.objects.filter(project_id=project_id)

    arr = None
    for data in raw_data:
        arr = data

    # This query provides an employee creation form
    employee = Employee.objects.filter(user_id=request.user.id)
    employee_arr = None
    for data in employee:
        employee_arr = data

    reference_task = Task.objects.filter(task_id=task_id)
    reference_task_arr = None
    for data in reference_task:
        reference_task_arr = data

    if request.method == "POST":
        creation_form = CreateTaskForm(data=request.POST)

        if creation_form.is_valid():
            code = creation_form.cleaned_data['code']
            name = creation_form.cleaned_data['name']
            description = creation_form.cleaned_data['description']
            responsible = creation_form.cleaned_data['responsible']
            initiator = creation_form.cleaned_data['initiator']
            state = creation_form.cleaned_data['state']
            priority = creation_form.cleaned_data['priority']
            type_task = creation_form.cleaned_data['type']
            date_deadline = creation_form.cleaned_data['date_deadline']

            task = Task(code=code, name=name, description=description, responsible=responsible, initiator=initiator,
                        state=state, priority=priority, type=type_task, date_deadline=date_deadline, project=arr,
                        manager=employee_arr)
            task.save()

            subtask = SubTasks(task=task, reference_task=reference_task_arr)
            subtask.save()

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            messages.error(request, "Ошибка при вводе данных")
    else:
        creation_form = CreateTaskForm()

        # Use a many-to-many query
        creation_form.fields['responsible'].queryset = Employee.objects.filter(projects=project_id)
        creation_form.fields['initiator'].queryset = Employee.objects.filter(projects=project_id)

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма создания новой подзадачи',
        'form': creation_form,
        'text_button': 'Создать подзадачу',
        'show_choose_project': 0,
        'project_id': project_id,
    })


# This view allows user edit your task (only for administrators)
def edit_task(request, project_id, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    instance = get_object_or_404(Task, task_id=task_id)
    form = CreateTaskForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    raw_data = Task.objects.raw(
        raw_query=f"SELECT * FROM tracking_dev_task where is_activate=True and project_id={project_id}"
    )

    return render(request, 'include/base_form.html', {
        'title_page': 'Форма редактирования задачи',
        'form': form,
        'text_button': 'Сохранить изменения',
        'show_choose_project': 0,
        'project_id': project_id,
    })


# This method allows user to add the data
def create_employee(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if request.method == "POST":
        creation_form = CreateEmployeeForm(data=request.POST)
        if creation_form.is_valid():
            post = creation_form.cleaned_data['post']
            description = creation_form.cleaned_data['description']

            employee = Employee(post=post, description=description, user_id=request.user.id)
            employee.save()

            return redirect(reverse('main_page'))
    else:
        creation_form = CreateEmployeeForm()

    return render(request, "include/base_form_auth.html", {
        'title_page': 'Форма заполнения данных о себе',
        'show_choose_project': 0,
        'form': creation_form,
        'text_button': 'Создать сотрудника'
    })


# This method allows user search and add new participants to project.
def search(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    results = []
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'

        results = Employee.objects.raw(
            raw_query=f"select * from tracking_dev_employee tde join auth_user au "
                      f"on tde.user_id = au.id where tde.is_activate and au.username='{query}';"
        )

    raw_data = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, 'include/user_search.html', {
        'title_page': 'Найденные сотрудники',
        'participants': results,
        'show_choose_project': 0,
        'list_projects': raw_data,
        'show_list_group': 0,
        'is_project_zone': 1,
        'project_id': project_id
    })


# This view allows user search tasks for the sprint
def task_sprint_search(request, project_id, sprint_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not is_user_in_this_project(request, project_id):
        return HttpResponseForbidden()

    results = []
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'

        results = Task.objects.raw(
            raw_query=f"select * from tracking_dev_task tdt "
                      f"join tracking_dev_state tds on tdt.state_id = tds.state_id "
                      f"where tds.\"isClosed\" = false and tdt.is_activate "
                      f"and (strpos(lower(tdt.code), lower('{query}')) > 0 or strpos(lower(tdt.\"name\"), "
                      f"lower('{query}')) > 0 "
                      f"or strpos(lower(tdt.description), lower('{query}')) > 0);"
        )

    raw_data = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, 'include/task_search.html', {
        'title_page': 'Найденные задачи',
        'tasks': results,
        'show_choose_project': 0,
        'list_projects': raw_data,
        'show_list_group': 0,
        'is_project_zone': 1,
        'project_id': project_id,
        'sprint_id': sprint_id
    })


# This function provides ajax for the vote button
def vote(request, project_id, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not is_user_in_this_project(request, project_id):
        return HttpResponseForbidden()

    # As we send data to the server we must use the POST.
    if request.method == "POST":
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            # Now we need check if the current user has voted
            employee_id_list = Employee.objects.filter(user_id=request.user.id)
            employee_id = 0

            # Go in the cycle
            for current_employee in employee_id_list:
                employee_id = current_employee.employee_id

            # Add the check if the current user has voted to the task.
            user_voted = Employee.objects.raw(
                raw_query=f"select * from tracking_dev_task_employee tdte "
                          f"where tdte.employee_id = {employee_id} and tdte.task_id = {task_id}"
            )

            # User has voted—the variable is 0. In the another side, this variable is 1.
            is_user_vote = 0

            # If the user has voted to the task, we should unlike.
            if len(list(user_voted)) > 0:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(f"delete from tracking_dev_task_employee tdte "
                                       f"WHERE tdte.task_id={task_id} and tdte.employee_id={employee_id}")
                except:
                    print("Can not delete the data")
            else:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(f"insert into tracking_dev_task_employee(task_id, employee_id) "
                                       f"values ({task_id}, {employee_id})")
                    connection.commit()
                except:
                    print("The user can not add to the database")
                is_user_vote = 1

            count_votes = Employee.objects.raw(
                raw_query=f"select tdte.id, tdte.employee_id, au.first_name, au.last_name, "
                          f"tde.post from tracking_dev_task_employee tdte "
                          f"join tracking_dev_employee tde on tde.employee_id = tdte.employee_id "
                          f"join auth_user au on au.id = tde.user_id  "
                          f"where tdte.task_id = {task_id}"
            )

            data = {
                "is_user_vote": is_user_vote,
                "count_votes": len(count_votes)
            }

            list_employee = []

            if len(count_votes) > 0:
                for employee in count_votes:
                    item = {
                        "employee_id": employee.employee_id,
                        "first_name": employee.first_name,
                        "last_name": employee.last_name,
                        "working": employee.post
                    }

                    list_employee.append(item)

            return JsonResponse({'data': data, 'list_employee': list_employee})
    return JsonResponse({'data': {}, 'list_employee': []})


# This view allows user search projects in the list of projects.
def project_search(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if request.method == "GET":
        # If the type is GET, we need check if request is ajax.
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            series = request.GET.get('series')
            if series != '':
                query_se = Project.objects.raw(
                    raw_query=f"select tdp.project_id, tdp.\"name\",  strpos(lower(tdp.code), lower('{series}')) "
                              f"as project_exists, strpos(lower(tdp.code), lower('{series}')) as code_exists, "
                              f"strpos(lower(tdp.description), lower('{series}')) as description_exists "
                              f"from tracking_dev_project tdp WHERE tdp.is_activate=True"
                )
            else:
                query_se = Project.objects.raw(
                    raw_query=f"select tdp.project_id, tdp.\"name\", 1 "
                              f"as project_exists, 1 as code_exists, "
                              f"1 as description_exists "
                              f"from tracking_dev_project tdp WHERE tdp.is_activate=True"
                )

            if len(query_se) > 0:
                data = []
                for position in query_se:
                    item = {
                        "project_id": position.project_id,
                        "code": position.code,
                        "date_create": position.date_create,
                        "description": position.description,
                        "code_exists": position.code_exists,
                        "project_exists": position.project_exists,
                        "description_exists": position.description_exists
                    }

                    data.append(item)
                res = data
            else:
                res = []

            return JsonResponse({'data': res})
    return JsonResponse({'data': []})


# This view provides sprint search
def sprint_search(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not is_user_in_this_project(request, project_id):
        return HttpResponseForbidden()

    if request.method == "GET":
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            series = request.GET.get('series')
            if series != '':
                query_se = Project.objects.raw(
                    raw_query=f"select *,"
                              f"strpos(lower(tds.\"name\"), lower('{series}')) as name_exists, "
                              f"strpos(lower(tds.description), lower('{series}')) "
                              f"as description_exists from tracking_dev_sprint tds "
                              f"where tds.project_id = {project_id} and tds.is_activate ;"
                )
            else:
                query_se = Project.objects.raw(
                    raw_query=f"select *, "
                              f"1 as name_exists, 1 as description_exists from tracking_dev_sprint tds "
                              f"where tds.project_id = {project_id} and tds.is_activate ;"
                )

            if len(query_se) > 0:
                data = []
                for position in query_se:
                    item = {
                        "sprint_id": position.sprint_id,
                        "project_id": project_id,
                        "name": position.name,
                        "date_create": position.date_create,
                        "description": position.description,
                        "name_exists": position.name_exists,
                        "description_exists": position.description_exists,
                        "date_start": position.date_start,
                        "date_end": position.date_end
                    }

                    data.append(item)
                res = data
            else:
                res = []

            return JsonResponse({'data': res})
    return JsonResponse({'data': []})


# This method allows users search the states
def state_search(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if request.method == "GET":
        # If the type is GET, we need check if request is ajax.
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            series = request.GET.get('series')
            if series != '':
                query_se = State.objects.raw(
                    raw_query=f"select tds.state_id, tds.\"name\",  "
                              f"strpos(lower(tds.\"name\"), lower('{series}')) as state_exists, "
                              f"strpos(lower(tds.code), lower('{series}')) as code_exists, "
                              f"strpos(lower(tds.description), lower('{series}')) as description_exists "
                              f"from tracking_dev_state tds WHERE tds.is_activate=True"
                )
            else:
                query_se = State.objects.raw(
                    raw_query=f"select tds.state_id, tds.\"name\", 1 as state_exists, "
                              f"1 as code_exists, 1 as description_exists from tracking_dev_state tds "
                              f"WHERE tds.is_activate=True"
                )

            if len(query_se) > 0:
                data = []
                for position in query_se:
                    item = {
                        "state_id": position.state_id,
                        "code": position.code,
                        "date_create": position.date_create,
                        "description": position.description,
                        "code_exists": position.code_exists,
                        "state_exists": position.state_exists,
                        "description_exists": position.description_exists
                    }

                    data.append(item)
                res = data
            else:
                res = []

            return JsonResponse({'data': res})
    return JsonResponse({'data': []})


# This view allows user search employee
def employee_search(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if request.method == "GET":
        # If the type is GET, we need check if request is ajax.
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            series = request.GET.get('series')
            if series != '':
                query_se = Employee.objects.raw(
                    raw_query=f"select au.first_name, au.last_name, tde.employee_id, tde.post, tde.description, tde.date_create, "
                              f"strpos(lower(au.first_name), lower('{series}')) as name_exists, "
                              f"strpos(lower(au.last_name), lower('{series}')) as surname_exists, "
                              f"strpos(lower(au.username), lower('{series}')) as username_exists, "
                              f"strpos(lower(tde.description), lower('{series}')) as description_exists "
                              f"from tracking_dev_employee tde join auth_user au on au.id = tde.user_id "
                              f"where tde.is_activate=True;"
                )
            else:
                query_se = Employee.objects.raw(
                    raw_query=f"select au.first_name, au.last_name, tde.employee_id, tde.post, "
                              f"tde.description, tde.date_create, "
                              f"1 as name_exists, 1 as surname_exists, 1 as username_exists, "
                              f"1 as description_exists from tracking_dev_employee tde join auth_user au "
                              f"on au.id = tde.user_id where tde.is_activate=True;"
                )

            if len(query_se) > 0:
                data = []
                for position in query_se:
                    item = {
                        "employee_id": position.employee_id,
                        "first_name": position.first_name,
                        "date_create": position.date_create,
                        "last_name": position.last_name,
                        "description": position.description,
                        "name_exists": position.name_exists,
                        "surname_exists": position.surname_exists,
                        "description_exists": position.description_exists
                    }

                    data.append(item)
                res = data
            else:
                res = []

            return JsonResponse({'data': res})
    return JsonResponse({'data': []})


def priority_search(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if request.method == "GET":
        # If the type is GET, we need check if request is ajax.
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            series = request.GET.get('series')
            if series != '':
                query_se = Priority.objects.raw(
                    raw_query=f"select *, strpos(lower(tdp.code), lower('{series}')) as code_exists, "
                              f"strpos(lower(tdp.\"name\"), lower('{series}')) as name_exists, "
                              f"strpos(lower(tdp.description), lower('{series}')) "
                              f"as description_exists from tracking_dev_priority tdp "
                              f"WHERE tdp.is_activate=True"
                )
            else:
                query_se = Priority.objects.raw(
                    raw_query=f"select *, 1 as code_exists, 1 as name_exists, 1 as description_exists "
                              f"from tracking_dev_priority tdp WHERE tdp.is_activate=True"
                )

            if len(query_se) > 0:
                data = []
                for position in query_se:
                    item = {
                        "priority_id": position.priority_id,
                        "code": position.code,
                        "name": position.name,
                        "date_create": position.date_create,
                        "description": position.description,
                        "code_exists": position.code_exists,
                        "name_exists": position.name_exists,
                        "description_exists": position.description_exists
                    }

                    data.append(item)
                res = data
            else:
                res = []

            return JsonResponse({'data': res})
    return JsonResponse({'data': []})


# This view provides type tasks search form
def type_search(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if request.method == "GET":
        # If the type is GET, we need check if request is ajax.
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            series = request.GET.get('series')
            if series != '':
                query_se = TypeTask.objects.raw(
                    raw_query=f"select *, "
                              f"strpos(lower(tdp.code), lower('{series}')) as code_exists, "
                              f"strpos(lower(tdp.\"name\"), lower('{series}')) as name_exists, "
                              f"strpos(lower(tdp.description), lower('{series}')) "
                              f"as description_exists from tracking_dev_typetask tdp "
                              f"WHERE tdp.is_activate=True"
                )
            else:
                query_se = TypeTask.objects.raw(
                    raw_query=f"select *, 1 as code_exists, "
                              f"1 as name_exists, 1 as description_exists from tracking_dev_typetask tdp "
                              f"WHERE tdp.is_activate=True"
                )

            if len(query_se) > 0:
                data = []
                for position in query_se:
                    item = {
                        "type_id": position.type_id,
                        "code": position.code,
                        "name": position.name,
                        "date_create": position.date_create,
                        "description": position.description,
                        "code_exists": position.code_exists,
                        "name_exists": position.name_exists,
                        "description_exists": position.description_exists
                    }

                    data.append(item)
                res = data
            else:
                res = []

            return JsonResponse({'data': res})
    return JsonResponse({'data': []})


def add_data(tasks, href, text_link):
    data = [href, text_link]
    for position in tasks:
        item = {
            "task_id": position.task_id,
            "code": position.code,
            "name": position.name,
            "project_id": position.project_id,
            "date_create": position.date_create,
            "description": position.description,
            "code_exists": position.code_exists,
            "name_exists": position.name_exists,
            "description_exists": position.description_exists
        }

        data.append(item)

    return data


# This method allows user search the tasks
def search_tasks(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not is_user_in_this_project(request, project_id):
        return HttpResponseForbidden()

    if request.method == "GET":
        # If the type is GET, we need check if request is ajax.
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            series = request.GET.get('series')
            if series != '':
                # Tasks, which needs to complete (which user is responsible)
                tasks_personal = Task.objects.raw(
                    raw_query=f"select *, strpos(lower(tdt.code), lower('{series}')) as code_exists, "
                              f"strpos(lower(tdt.\"name\"), lower('{series}')) as name_exists, "
                              f"strpos(lower(tdt.description), lower('{series}')) as description_exists "
                              f"from tracking_dev_task tdt "
                              f"join tracking_dev_employee tde on tdt.responsible_id = tde.employee_id "
                              f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                              f"where tdt.is_activate and tds.\"isClosed\" = false and tde.user_id = {request.user.id} "
                              f"and tdt.project_id = {project_id} and tdt.is_activate=True;"
                )

                tasks_controller = Task.objects.raw(
                    raw_query=f"select *, strpos(lower(tdt.code), lower('{series}')) as code_exists, "
                              f"strpos(lower(tdt.\"name\"), lower('{series}')) as name_exists, "
                              f"strpos(lower(tdt.description), lower('{series}')) as description_exists "
                              f"from tracking_dev_task tdt "
                              f"join tracking_dev_employee tde on tdt.manager_id = tde.employee_id "
                              f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                              f"where tdt.is_activate and tds.\"isClosed\" = false and tde.user_id = {request.user.id} "
                              f"and tdt.project_id = {project_id} and tdt.is_activate=True;"
                )

                # Tasks, in which current user is observer
                tasks_observer = Task.objects.raw(
                    raw_query=f"select *, "
                              f"strpos(lower(tdt.code), lower('{series}')) as code_exists, "
                              f"strpos(lower(tdt.\"name\"), lower('{series}')) as name_exists, "
                              f"strpos(lower(tdt.description), lower('{series}')) as description_exists "
                              f"from tracking_dev_task tdt "
                              f"join tracking_dev_employee tde on tdt.initiator_id = tde.employee_id "
                              f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                              f"where tde.user_id = {request.user.id} and tdt.project_id = {project_id} and tdt.is_activate "
                              f"and tds.\"isClosed\" = false and tdt.is_activate=True;"
                )

                # Another tasks
                tasks_list = Task.objects.raw(
                    raw_query=f"select *, "
                              f"strpos(lower(tdt.code), lower('{series}')) as code_exists, "
                              f"strpos(lower(tdt.\"name\"), lower('{series}')) as name_exists, "
                              f"strpos(lower(tdt.description), lower('{series}')) as description_exists "
                              f"from tracking_dev_task tdt "
                              f"join tracking_dev_employee tde on tdt.initiator_id = tde.employee_id "
                              f"join tracking_dev_employee tde2 on tdt.responsible_id = tde2.employee_id "
                              f"join tracking_dev_employee tde3 on tdt.manager_id = tde3.employee_id "
                              f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                              f"where tde.user_id != {request.user.id} and tdt.project_id = {project_id} "
                              f"and tde2.user_id != {request.user.id} and tdt.is_activate "
                              f"and tde3.user_id != {request.user.id} "
                              f"and tds.\"isClosed\" = false and tdt.is_activate=True;"
                )
            else:
                # Tasks, which needs to complete (which user is responsible)
                tasks_personal = Task.objects.raw(
                    raw_query=f"select *, 1 as code_exists, 1 as name_exists, 1 as description_exists from tracking_dev_task tdt "
                              f"join tracking_dev_employee tde on tdt.responsible_id = tde.employee_id "
                              f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                              f"where tdt.is_activate and tds.\"isClosed\" = false and tde.user_id = {request.user.id} "
                              f"and tdt.project_id = {project_id} and tdt.is_activate=True;"
                )

                tasks_controller = Task.objects.raw(
                    raw_query=f"select *, 1 as code_exists, 1 as name_exists, 1 as description_exists from tracking_dev_task tdt "
                              f"join tracking_dev_employee tde on tdt.manager_id = tde.employee_id "
                              f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                              f"where tdt.is_activate and tds.\"isClosed\" = false and tde.user_id = {request.user.id} "
                              f"and tdt.project_id = {project_id} and tdt.is_activate=True;"
                )

                # Tasks, in which current user is observer
                tasks_observer = Task.objects.raw(
                    raw_query=f"select *, 1 as code_exists, 1 as name_exists, 1 as description_exists from tracking_dev_task tdt "
                              f"join tracking_dev_employee tde on tdt.initiator_id = tde.employee_id "
                              f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                              f"where tde.user_id = {request.user.id} and tdt.project_id = {project_id} and tdt.is_activate "
                              f"and tds.\"isClosed\" = false and tdt.is_activate=True;"
                )

                # Another tasks
                tasks_list = Task.objects.raw(
                    raw_query=f"select *, 1 as code_exists, 1 as name_exists, 1 as description_exists "
                              f"from tracking_dev_task tdt "
                              f"join tracking_dev_employee tde on tdt.initiator_id = tde.employee_id "
                              f"join tracking_dev_employee tde2 on tdt.responsible_id = tde2.employee_id "
                              f"join tracking_dev_employee tde3 on tdt.manager_id = tde3.employee_id "
                              f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                              f"where tde.user_id != {request.user.id} and tdt.project_id = {project_id} "
                              f"and tde2.user_id != {request.user.id} and tdt.is_activate "
                              f"and tde3.user_id != {request.user.id} "
                              f"and tds.\"isClosed\" = false and tdt.is_activate=True;"
                )

            if len(tasks_personal) > 0 or len(tasks_observer) > 0 or len(tasks_list) > 0:
                data = [add_data(tasks_personal, "collapseExample_personal", "Задачи, в которых Вы ответственный"),
                        add_data(tasks_controller, "collapseExample_controller", "Задачи, в которых Вы проверяющий"),
                        add_data(tasks_observer, "collapseExample_observer", "Задачи, в которых Вы наблюдатель"),
                        add_data(tasks_list, "collapseExample_all", "Все остальные задачи")]
                res = data
            else:
                res = []

            return JsonResponse({'data': res, 'project_id': project_id})
    return JsonResponse({'data': [], 'project_id': project_id})


def search_collabarators(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not is_user_in_this_project(request, project_id):
        return HttpResponseForbidden()

    if request.method == "GET":
        # If the type is GET, we need check if request is ajax.
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            series = request.GET.get('series')
            if series != '':
                query_se = Project.objects.raw(
                    raw_query=f"select *, au.id as user_id, "
                              f"strpos(lower(au.first_name), lower('{series}')) as name_exists, "
                              f"strpos(lower(au.last_name), lower('{series}')) as last_name_exists "
                              f"from tracking_dev_employee_projects tdep "
                              f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                              f"join auth_user au on tde.user_id = au.id "
                              f"where tdep.project_id={project_id} and tdep.is_activate=True"
                )
            else:
                query_se = Project.objects.raw(
                    raw_query=f"select *, au.id as user_id, 1 as name_exists, 1 as last_name_exists "
                              f"from tracking_dev_employee_projects tdep "
                              f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                              f"join auth_user au on tde.user_id = au.id "
                              f"where tdep.project_id={project_id} and tdep.is_activate=True"
                )

            if len(query_se) > 0:
                data = []
                for position in query_se:
                    item = {
                        "employee_id": position.employee_id,
                        "project_id": position.project_id,
                        "user_id": position.user_id,
                        "first_name": position.first_name,
                        "last_name": position.last_name,
                        "email": position.email,
                        "post": position.post,
                        "name_exists": position.name_exists,
                        "last_name_exists": position.last_name_exists
                    }

                    data.append(item)
                res = data
            else:
                res = []

            return JsonResponse({'data': res, 'project_id': project_id, "user_id": request.user.id,
                                 'is_admin_zone': request.user.is_staff})
    return JsonResponse({'data': [], 'project_id': project_id, "user_id": request.user.id,
                         'is_admin_zone': request.user.is_staff})


# This method adds new users to the project
def add_employee_to_project(request, project_id, employee_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"insert into tracking_dev_employee_projects(employee_id, project_id, is_activate) "
                           f"values ({employee_id}, {project_id}, True)")
    except:
        print("Can not add the participant")
    finally:
        return redirect(reverse("collabs", kwargs={'project_id': project_id}))


# This view allows user add the task to sprint
def add_task_to_sprint(request, project_id, sprint_id, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if (not request.user.is_staff) or (not is_user_in_this_project(request, project_id)):
        return HttpResponseForbidden()

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"insert into tracking_dev_sprint_task(sprint_id, task_id) "
                           f"values ({sprint_id}, {task_id})")
    except:
        print("Can not add the task to the sprint")
    finally:
        return redirect(reverse('sprint_description', kwargs={'project_id': project_id, 'sprint_id': sprint_id}))


# This method allows users login
def login(request):
    if request.user.is_authenticated:
        return HttpResponseNotFound()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('main_page'))
            else:
                messages.error(request, "Incorrect name or password")
        else:
            messages.error(request, "Error in the inputting login data")
    else:
        form = LoginForm()

    return render(request, "include/base_form.html", {
        'form': form,
        'title_page': 'Форма авторизации',
        'text_button': 'Авторизоваться'
    })


# This method allows user logout from system
def logout(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    auth.logout(request)
    return redirect(reverse('main_page'))


# This method allows sign up to system
def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            mail = form.cleaned_data['email']
            is_user_exists_with_mail = User.objects.filter(email=mail)

            if is_user_exists_with_mail.exists():
                messages.error(request, "Данная электронная почта существует. Пожалуйста, введите другую почту")
            else:
                new_user = form.save()
                auth.login(request, new_user)

                # Need to redirect to another form with employee create
                return redirect(reverse('create_employee'))
        else:
            messages.error(request, "Ошибка в вводе данных")
    else:
        form = UserRegistrationForm()

    return render(request, "include/base_form_auth.html", {
        'form': form,
        'title_page': 'Форма регистрации',
        'text_button': 'Зарегистрироваться',
        'step': 1
    })


# This method marks the task to complete
def mark_as_completed(request, project_id, task_id):
    # if the user ia not authenticated, then it cannot delete
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if not is_user_in_this_project(request, project_id):
        return HttpResponseForbidden()

    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE tracking_dev_task SET state_id=5 WHERE "
                       f"project_id={project_id} and task_id={task_id}")

    return redirect(reverse('tasks_for_project', kwargs={'project_id': project_id}))


# This view provides a report of the completed tasks by deadline dates.
def calculate_report_tasks(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    un_completed_tasks = Task.objects.raw(
        raw_query=f"select 1 as task_id, to_char(date_deadline, 'Month') as char_month, extract(month from date_deadline) as number_month, "
                  f"extract (year from date_deadline) as number_year, count(tdt.task_id) as count_tasks "
                  f"from tracking_dev_task tdt "
                  f"join tracking_dev_state tds on tdt.state_id = tds.state_id "
                  f"where tds.\"isClosed\" = false and tdt.is_activate and tdt.project_id = {project_id} "
                  f"group by number_month, number_year, char_month order by number_year, number_month "
    )

    completed_tasks = Task.objects.raw(
        raw_query=f"select 1 as task_id, to_char(date_deadline, 'Month') as char_month, extract(month from date_deadline) as number_month, "
                  f"extract (year from date_deadline) as number_year, count(tdt.task_id) as count_tasks "
                  f"from tracking_dev_task tdt "
                  f"join tracking_dev_state tds on tdt.state_id = tds.state_id "
                  f"where tds.\"isClosed\" = true and tdt.is_activate and tdt.project_id = {project_id} "
                  f"group by number_month, number_year, char_month order by number_year, number_month "
    )

    raw_query = f'select 1 as task_id, COUNT(tdt.task_id) as count_elems, tds."name" as curr_state ' \
                f'from tracking_dev_task tdt join tracking_dev_state tds on tdt.state_id = tds.state_id ' \
                f'where tdt.is_activate = true and tdt.project_id = {project_id} ' \
                f'group by tds."name"'

    random_colors_array = []
    r = lambda: random.randint(0, 255)

    for data in raw_query:
        random_colors_array.append('#%02X%02X%02X' % (r(), r(), r()))

    count_tasks_by_states = Task.objects.raw(
        raw_query=raw_query
    )

    raw_data = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/report.html", {
        'un_completed_tasks': un_completed_tasks,
        'completed_tasks': completed_tasks,
        'count_tasks_by_states': count_tasks_by_states,
        'is_project_zone': 1,
        'list_projects': raw_data,
        'colors': random_colors_array
    })


# This view provides laboriousness report by user
def report_by_laboriousness(request, project_id, sprint_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    sum_capacity_plan_fact = Laboriousness.objects.raw(
        raw_query=f"select 1 as laboriousness_id, SUM(tdl.capacity_plan) as sum_plan, SUM(tdl.capacity_fact) as sum_fact, "
                  f"tdl.employee_id as employee_id, au.first_name as employee_name, "
                  f"au.last_name as employee_surname from tracking_dev_laboriousness tdl "
                  f"join tracking_dev_task tdt on tdl.task_id = tdt.task_id "
                  f"join tracking_dev_employee tde on tdl.employee_id = tde.employee_id "
                  f"join auth_user au on au.id = tde.user_id "
                  f"where tdl.task_id in (select tdst.task_id  from tracking_dev_sprint_task tdst where tdst.sprint_id = {sprint_id}) "
                  f"and tdl.task_id in (select tdt2.task_id from tracking_dev_task tdt2 where tdt2.project_id = {project_id}) "
                  f"group by tdl.employee_id, au.first_name, au.last_name"
    )

    raw_data = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    details_data = Laboriousness.objects.raw(
        raw_query=f"select 1 as laboriousness_id, tdt.code as task_code, tdt.task_id as task_id,"
                  f"au.first_name as employee_name, au.last_name as surname_employee, "
                  f"tdl.capacity_plan as plan, tdl.capacity_fact as fact from tracking_dev_laboriousness tdl "
                  f"join tracking_dev_task tdt on tdl.task_id = tdt.task_id "
                  f"join tracking_dev_employee tde on tde.employee_id = tdl.employee_id "
                  f"join auth_user au on au.id = tde.user_id "
                  f"where tdl.task_id in (select tdst.task_id from "
                  f"tracking_dev_sprint_task tdst where tdst.sprint_id={sprint_id}) "
                  f"and tdl.task_id in (select tdt2.task_id from tracking_dev_task "
                  f"tdt2 where tdt2.project_id = {project_id}) order by au.first_name, au.last_name"
    )

    r = lambda: random.randint(0, 255)

    random_color_plan = '#%02X%02X%02X' % (r(), r(), r())
    random_color_fact = '#%02X%02X%02X' % (r(), r(), r())

    random_colors_array_plan = [random_color_plan for i in range(len(list(sum_capacity_plan_fact)))]
    random_colors_array_fact = [random_color_fact for i in range(len(list(sum_capacity_plan_fact)))]

    return render(request, "include/report_laboriousness.html", {
        'capacity': sum_capacity_plan_fact,
        'is_project_zone': 1,
        'random_colors_array_plan': random_colors_array_plan,
        'random_colors_array_fact': random_colors_array_fact,
        'count_users': len(list(sum_capacity_plan_fact)),
        'list_projects': raw_data,
        'project_id': project_id,
        'details_data': details_data
    })


# This view provides the report of the user
def report_by_employee(request, project_id, employee_id):
    # This report query provides list of the count tasks on the different states.
    count_tasks_by_states = Task.objects.raw(
        raw_query=f"select 1 as task_id, tds.\"name\" as name_state , COUNT(tdt.task_id) as count_tasks from tracking_dev_task tdt "
                  f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                  f"where tdt.project_id = {project_id} and tdt.responsible_id = {employee_id} "
                  f"and tdt.is_activate = true "
                  f"group by tds.\"name\""
    )

    # This report query provides count completed tasks by month
    count_completed_tasks_by_month = Task.objects.raw(
        raw_query=f"select 1 as task_id, to_char(date_deadline, 'Month') as char_month, extract(month from date_deadline) as number_month, "
                  f"extract (year from date_deadline) as number_year, count(tdt.task_id) as count_tasks from tracking_dev_task tdt "
                  f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                  f"where tdt.responsible_id = {employee_id} and tdt.project_id = {project_id} "
                  f"and tds.\"isClosed\" = true and tdt.is_activate = true "
                  f"group by number_month , number_year, char_month order by number_year , number_month ;"
    )

    # This report query provides not completed tasks by month
    count_uncompleted_tasks_by_month = Task.objects.raw(
        raw_query=f"select 1 as task_id, to_char(date_deadline, 'Month') as char_month, extract(month from date_deadline) as number_month, "
                  f"extract (year from date_deadline) as number_year, count(tdt.task_id) as count_tasks from tracking_dev_task tdt "
                  f"join tracking_dev_state tds on tds.state_id = tdt.state_id "
                  f"where tdt.responsible_id = {employee_id} and tdt.project_id = {project_id} "
                  f"and tds.\"isClosed\" = false and tdt.is_activate = true "
                  f"group by number_month , number_year, char_month order by number_year , number_month ;"
    )

    user_description = Employee.objects.raw(
        raw_query=f"select * from tracking_dev_employee tde "
                  f"join auth_user au ON tde.user_id = au.id where tde.employee_id = {employee_id}"
    )

    random_colors_array = []
    r = lambda: random.randint(0, 255)

    for data in count_tasks_by_states:
        random_colors_array.append('#%02X%02X%02X' % (r(), r(), r()))

    raw_data = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/report_employee.html", {
        'un_completed_tasks': count_uncompleted_tasks_by_month,
        'completed_tasks': count_completed_tasks_by_month,
        'count_tasks_by_states': count_tasks_by_states,
        'user_info': user_description,
        'list_projects': raw_data,
        'is_project_zone': 1,
        'colors': random_colors_array,
        'project_id': project_id,
        'employee_id': employee_id
    })


# This view provides a list of the completed or uncompleted tasks
def show_uncompleted_tasks_by_user(request, project_id, employee_id, sort):
    query = f"select * from tracking_dev_task tdt join tracking_dev_state tds on tdt.state_id = tds.state_id " \
            f"where tdt.project_id = {project_id} and tdt.responsible_id = {employee_id} "

    if sort == "uncompleted":
        query += "and tds.\"isClosed\" = false "
    else:
        query += "and tds.\"isClosed\" = true "

    count_tasks = Task.objects.raw(raw_query=query)

    raw_data = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/list_data/task_compact.html", {
        "count_tasks": count_tasks,
        'is_project_zone': 1,
        'list_projects': raw_data,
        'project_id': project_id
    })


# This view provides a kanban board manager
def kanban_board_manager(request, project_id):
    data = State.objects.filter(is_activate=True).order_by('isClosed')
    tasks_by_state = []
    for elem in data:
        tasks_query = Task.objects.raw(
            raw_query=f"select * from tracking_dev_task tdt "
                      f"join tracking_dev_employee tde on tde.employee_id = tdt.responsible_id "
                      f"join auth_user au on au.id = tde.user_id "
                      f"where tdt.state_id = {elem.state_id} and tdt.project_id = {project_id} and tdt.is_activate = true;"
        )

        my_dict = {
            "state": elem.name,
            "description": elem.description,
            "tasks": tasks_query
        }

        tasks_by_state.append(my_dict)

    raw_data = Project.objects.raw(
        raw_query=f"select * from tracking_dev_employee_projects tdep "
                  f"join tracking_dev_employee tde on tdep.employee_id = tde.employee_id "
                  f"join tracking_dev_project tdp on tdp.project_id = tdep.project_id "
                  f"where tde.user_id = {request.user.id};"
    )

    return render(request, "include/kanban.html", {
        'list_states': data,
        'tasks_by_state': tasks_by_state,
        'project_id': project_id,
        # The project zone variable can implement fast access to functions of the project.
        'is_project_zone': 1,
        'list_projects': raw_data
    })
