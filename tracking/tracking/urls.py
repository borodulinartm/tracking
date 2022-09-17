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
    path('main_page/projects/<int:project_id>', project_description, name="project_description"),

    path('main_page/states', get_state_list, name="states"),
    path('main_page/states/<int:state_id>', state_description, name="state_description"),

    path('main_page/priorities', get_priority_list, name="priorities"),
    path('main_page/priorities/<int:priority_id>', priority_description, name="priority_description"),

    path('main_page/types', type_task_list, name="types"),
    path('main_page/types/<int:type_id>', type_task_description, name="type_description"),

    path('main_page/employees', employee_list, name="employees"),
    path('main_page/employees/<int:employee_id>', employee_description, name="employee_description")
]

