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
    path('main_page/projects/<int:project_id>/report', calculate_report_tasks, name="project_report"),

    path('main_page/projects/<int:project_id>/sprints', get_sprint_list_for_project, name="sprints"),
    path('main_page/projects/<int:project_id>/sprints/<int:sprint_id>', sprint_description,
         name="sprint_description"),
    path('main_page/projects/<int:project_id>/sprints/<int:sprint_id>/edit', edit_sprint, name="sprint_edit"),
    path('main_page/projects/<int:project_id>/sprints/<int:sprint_id>/delete', sprint_remove, name="sprint_remove"),
    path('main_page/projects/<int:project_id>/sprints/<int:sprint_id>/delete_task/<int:task_id>',
         remove_task_from_sprint,
         name="remove_task_from_sprint"),
    path('main_page/projects/<int:project_id>/sprints/<int:sprint_id>/list_tasks', get_list_sprint_task,
         name="list_tasks_for_sprint"),

    path('main_page/projects/<int:project_id>/sprints/create', create_sprint, name="create_sprint"),
    path('main_page/projects/<int:project_id>/report_employee/<int:employee_id>', report_by_employee,
         name="employee_report"),
    path('main_page/projects/<int:project_id>/report_laboriousness/<int:sprint_id>',
         report_by_laboriousness, name="report_laboriousness"),
    path('main_page/projects/<int:project_id>/employee/<int:employee_id>/tasks/<str:sort>',
         show_uncompleted_tasks_by_user, name="uncompleted_tasks_by_user"),
    path('main_page/projects/<int:project_id>/delete', project_remove, name="project_delete"),
    path('main_page/projects<int:project_id>/collobarators', get_list_collobarators_to_project, name="collabs"),
    path('main_page/projects/<int:project_id>/collobarators/<int:employee_id>/delete', remove_user_from_current_project,
         name="delete_employee_from_project"),
    path('main_page/projects/<int:project_id>/collobarators/remove_all', remove_all_users_from_current_project,
         name="delete_all_employee_from_project"),
    path('main_page/projects/<int:project_id>/tasks', show_list_tasks_for_project, name="tasks_for_project"),
    path('main_page/projects/create', create_project, name="create_project"),
    path('main_page/projects/<int:project_id>/edit', edit_project, name="edit_project"),
    path('main_page/projects/<int:project_id>/kanban_viewer', kanban_board_manager, name="kanban_board"),

    path('main_page/states', get_state_list, name="states"),
    path('main_page/states/<int:state_id>', state_description, name="state_description"),
    path('main_page/states/create', create_state, name="create_state"),
    path('main_page/states/<int:state_id>/edit', edit_states, name="state_edit"),
    path('main_page/states/<int:state_id>/delete', state_remove, name="state_remove"),

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
    path('main_page/employees/<int:employee_id>/delete', employee_remove, name="employee_delete"),

    path('main_page/projects/<int:project_id>/tasks/<int:task_id>', task_description, name="task_description"),
    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/delete', task_remove, name="task_delete"),
    path('main_page/projects/<int:project_id>/tasks/create', create_task, name="task_create"),
    path('main_page/projects<int:project_id>/tasks/<int:task_id>/create_sub_task', create_subtask_form,
         name="subtask_create"),

    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/edit', edit_task, name="edit_task"),
    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/mark_as_read', mark_as_completed,
         name="mark_completed"),

    path('main_page/projects/<int:project_id>/collobarators/search', search, name="search"),
    path('main_page/projects/<int:project_id>/sprints/<int:sprint_id>/search', task_sprint_search,
         name="task_sprint_search"),
    path('main_page/finded_projects', project_search, name="project_search"),
    path('main_page/finded_states', state_search, name="state_search"),
    path('main_page/<int:project_id>/finded_sprints', sprint_search, name="sprint_search"),
    path('main_page/finded_employee', employee_search, name="employee_search"),
    path('main_page/finded_priority', priority_search, name="priority_search"),
    path('main_page/finded_type_task', type_search, name="type_search"),
    path('main_page/<int:project_id>/finded_task', search_tasks, name="task_search"),
    path('main_page/<int:project_id>/finded_collabs', search_collabarators, name="collabs_search"),
    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/vote', vote, name="vote"),

    path('main_page/projects/<int:project_id>/collobarators/add/<int:employee_id>', add_employee_to_project,
         name="add_user"),
    path('main_page/projects/<int:project_id>/sprints/<int:sprint_id>/add/<int:task_id>', add_task_to_sprint,
         name="add_task"),

    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/capacity', form_capacity_table, name="form_capacity"),
    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/capacity_delete/<int:employee_id>',
         remove_row_from_capacity_table, name="remove_capacity"),
    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/create_capacity', create_laboriousness,
         name="create_capacity"),
    path('main_page/projects/<int:project_id>/tasks/<int:task_id>/edit/<int:laboriousness_id>', edit_laboriousness,
         name="edit_laboriousness"),

    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
    path('main_page/employee/create', create_employee, name="create_employee")
]
