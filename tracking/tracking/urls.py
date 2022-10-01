"""tracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tracking_dev.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    # Страница - картотека проектов
    path('main_page', index, name="main_page"),

    path('main_page/projects', get_list_projects, name="projects"),
    path('main_page/projects/<int:project_id>', show_extra_functions, name="project_extra_function"),
    path('main_page/projects/<int:project_id>/description', project_description, name="project_description"),
    path('main_page/projects/<int:project_id>/delete', project_remove, name="project_delete"),
    path('main_page/projects<int:project_id>/collobarators', get_list_collobarators_to_project, name="collabs"),
    path('main_page/projects/<int:project_id>/collobarators/<int:employee_id>/delete', remove_user_from_current_project,
         name="delete_employee_from_project"),
    path('main_page/projects/<int:project_id>/collobarators/remove_all', remove_all_users_from_current_project,
         name="delete_all_employee_from_project"),
    path('main_page/projects/<int:project_id>/tasks', show_list_tasks_for_project, name="tasks_for_project"),
    path('main_page/projects/create', create_project, name="create_project"),
    path('main_page/projects/<int:project_id>/edit', edit_project, name="edit_project"),

    path('main_page/states', get_state_list, name="states"),
    path('main_page/states/<int:state_id>', state_description, name="state_description"),

    path('main_page/priorities', get_priority_list, name="priorities"),
    path('main_page/priorities/<int:priority_id>', priority_description, name="priority_description"),
    path('main_page/priorities/<int:priority_id>/delete', priority_remove, name="priority_delete"),
    path('main_page/priorities/create', create_priority, name="create_priority"),
    path('main_page/priorities<int:priority_id>/edit', edit_priority, name="edit_priority"),

    path('main_page/types', type_task_list, name="types"),
    path('main_page/types/<int:type_id>', type_task_description, name="type_description"),
    path('main_page/types<int:type_id>/delete', type_remove, name="type_remove"),
    path('main_page/types/create', create_type_task, name="create_type_task"),
    path('main_page/types/<int:type_id>/edit', edit_type_task, name="edit_type_task"),

    path('main_page/employees', employee_list, name="employees"),
    path('main_page/employees/<int:employee_id>', employee_description, name="employee_description"),
    path('main_page/employees<int:employee_id>/delete', employee_remove, name="employee_delete"),

    path('main_page/projects/<int:project_id>/tasks/<int:task_id>', task_description, name="task_description"),
    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/delete', task_remove, name="task_delete"),
    path('main_page/projects/<int:project_id>/tasks/create', create_task, name="task_create"),
    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/edit', edit_task, name="edit_task"),
    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/mark_as_read', mark_as_completed,
         name="mark_completed"),

    path('main_page/projects<int:project_id>/collobarators/search', search, name="search"),
    path('main_page/projects/<int:project_id>/collobarators/add/<int:employee_id>', add_employee_to_project,
         name="add_user"),

    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
    path('main_page/employee/create', create_employee, name="create_employee")
]
