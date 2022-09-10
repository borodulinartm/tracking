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

    def __str__(self):
        return str(self.project_id)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Project description"
