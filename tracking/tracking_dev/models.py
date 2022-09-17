import datetime

import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# Класс - картотека проектов
class Project(models.Model):
    # For the postgres sql if you want to create an autoincrement field, you should create auto field
    # By default, Django provides an ID, which got an autoincrement purpose.
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="hello_world")
    description = models.TextField(default='description of the project')
    # This field needs to add by default
    date_create = models.DateField(default=django.utils.timezone.now(), blank=True)
    code = models.CharField(max_length=50, default="default code")

    def __str__(self):
        return str(self.project_id)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Project description"


# Class—State of the tasks
class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, default="default code")
    date_create = models.DateField(default=django.utils.timezone.now(), blank=True)
    name = models.CharField(max_length=50, default="hello_world")
    isClosed = models.BooleanField(default=False)
    description = models.TextField(default="")

    def __str__(self):
        return str(self.state_id)

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "State description"


# Class—Priority of the Tasks
class Priority(models.Model):
    priority_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, default='default code')
    name = models.CharField(max_length=40, default='default name')
    description = models.TextField(default="")
    date_create = models.DateField(default=django.utils.timezone.now(), blank=True)

    def __str__(self):
        return str(self.priority_id)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priority description"


# Class-type of the tasks (new functionality, task, bug, test)
class TypeTask(models.Model):
    type_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, default='default code')
    name = models.CharField(max_length=40, default='default name')
    description = models.TextField(default="")
    date_create = models.DateField(default=django.utils.timezone.now(), blank=True)

    def __str__(self):
        return str(self.type_id)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Type description"
