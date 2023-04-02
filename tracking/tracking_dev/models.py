import datetime

import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from colorfield.fields import ColorField


class Profession(models.Model):
    profession_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, default="something_code")
    name = models.CharField(max_length=50, default="something")
    description = models.TextField(default='description of the text')
    salary = models.IntegerField(default=0)
    date_create = models.DateTimeField(blank=True, default=django.utils.timezone.now())
    date_update = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Profession"
        verbose_name_plural = "Profession description"


# Create your models here.
# Класс - картотека проектов
class Project(models.Model):
    # For the postgres sql if you want to create an autoincrement field, you should create auto field
    # By default, Django provides an ID, which got an autoincrement purpose.
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="hello_world")
    description = models.TextField(default='description of the project')
    # This field needs to add by default
    date_create = models.DateTimeField(blank=True, default=django.utils.timezone.now())
    # This field will be use when the field is updated
    date_change = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=50, default="default code")
    # Add extra fields (such as state of the project, budget, etc.)
    budget = models.IntegerField(default=0)
    date_deadline = models.DateField(default=django.utils.timezone.now())
    # Трудоёмкость проекта (в часах)
    laboriousness = models.IntegerField(default=0)
    # This field uses for deleting information from a database
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Project description"


# This model provides an employee, which extends user
# I can make the extent of the abstract user, but I don't make it
# because it is more simple.
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    description = models.TextField(default="the description of the post")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(default=django.utils.timezone.now(), blank=True)
    date_change = models.DateTimeField(auto_now=True)
    # Add Many-to-many relationship
    projects = models.ManyToManyField(Project, related_name="employee_projects")
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name="employee_profession", default=2)
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employee description"


# Class—State of the tasks
class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, default="default code")
    date_create = models.DateTimeField(default=django.utils.timezone.now(), blank=True)
    date_change = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50, default="hello_world")
    isClosed = models.BooleanField(default=False)
    projects = models.ManyToManyField(Project, related_name='project_state')

    # Добавляем дополнительное поле - % выполнения задачи в данном состоянии
    percentage = models.IntegerField(default=0)
    description = models.TextField(default="")
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "State description"


# Class—Priority of the Tasks
class Priority(models.Model):
    priority_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, default='default code')
    name = models.CharField(max_length=40, default='default name')
    description = models.TextField(default="")
    projects = models.ManyToManyField(Project, related_name='priority_project')
    date_create = models.DateField(blank=True, default=django.utils.timezone.now())
    date_change = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)

    priority_value = models.IntegerField(default=0)
    priority_color = ColorField(default="#FF0000")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priority description"


# Class-type of the tasks (new functionality, task, bug, test)
class TypeTask(models.Model):
    type_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, default='default code')
    name = models.CharField(max_length=40, default='default name')
    description = models.TextField(default="")
    date_create = models.DateTimeField(blank=True, default=django.utils.timezone.now())
    date_change = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)

    # Добавляем связь "многие-ко многим" к проектам
    projects = models.ManyToManyField(Project, related_name="typetask_projects")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Type description"


# This model provides an information about task
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, default="default code")
    name = models.CharField(max_length=50, default="default name")
    description = models.TextField(default="description of the task", blank=True)
    responsible = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name="r")  # This is a
    # person who must work
    initiator = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name="rr")  # A person, who
    # view the work responsible
    manager = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name="rrrrrrr", null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="rrr")
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, related_name="rrrr")
    type = models.ForeignKey(TypeTask, on_delete=models.CASCADE, related_name="rrrrr")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="rrrrrr")
    date_create = models.DateTimeField(default=django.utils.timezone.now(), blank=True)  # This date you cannot change
    date_change = models.DateTimeField(auto_now=True)  # This date you can change
    date_deadline = models.DateField(default=django.utils.timezone.now(), blank=True)
    is_activate = models.BooleanField(default=True)

    # Add the external field (Employee) - many-to-many relationship
    employee = models.ManyToManyField(Employee, related_name="task_votes")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Task description"


# This model provides sub-tasks for the tasks
class SubTasks(models.Model):
    sub_task_id = models.AutoField(primary_key=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name="r_task_id")
    reference_task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='r_task_description')

    def __str__(self):
        return str(self.sub_task_id)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Task description"


# This model provides sprint realization
class Sprint(models.Model):
    sprint_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, default="default code")
    name = models.CharField(max_length=50, default="default name")
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='r_project_id')
    description = models.TextField(default="description of the task", blank=True)
    date_create = models.DateTimeField(default=django.utils.timezone.now(), blank=True)  # This date you cannot change
    date_start = models.DateTimeField(default=django.utils.timezone.now())  # This date can change
    date_end = models.DateTimeField(default=django.utils.timezone.now())
    is_closed = models.BooleanField(default=False)
    is_activate = models.BooleanField(default=True)

    # Add the external field many-to-many relationship
    task = models.ManyToManyField(Task, related_name="employee_projects")

    def __str__(self):
        return str(self.sprint_id)

    class Meta:
        verbose_name = "Sprint"
        verbose_name_plural = "Sprint description"


# This model provides capacity for the task and person
class Laboriousness(models.Model):
    laboriousness_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='rr_employee_id')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='rr_task_id')
    capacity_plan = models.IntegerField(default=0)
    capacity_fact = models.IntegerField(default=0)

    def __str__(self):
        return str(self.laboriousness_id)

    class Meta:
        verbose_name = "Laboriousness"
        verbose_name_plural = "Laboriousness description"
