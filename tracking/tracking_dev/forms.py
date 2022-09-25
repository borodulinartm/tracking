from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


# The form creation method. Another forms will create the same as this form.
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your project name',
                                                                            'style': 'margin-bottom: 20px'}))
        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs=
                                                                           {'placeholder': 'Your description',
                                                                            'rows': '3',
                                                                            'style': 'margin-bottom: 20px'}))
        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'your code',
                                                                            'style': 'margin-bottom: 20px'}))

        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['code'].label = "Код"


# This class provides priority form
class CreatePriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['name', 'description', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your project name',
                                                                            'style': 'margin-bottom: 20px'}))
        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs=
                                                                           {'placeholder': 'Your description',
                                                                            'rows': '3',
                                                                            'style': 'margin-bottom: 20px'}))
        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'your code',
                                                                            'style': 'margin-bottom: 20px'}))

        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['code'].label = "Код"


# This form provides enter the types of the task form
class CreateTypeTaskForm(forms.ModelForm):
    class Meta:
        model = TypeTask
        fields = ['name', 'description', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Your type task name',
            'style': 'margin-bottom: 20px'}))
        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Description type of the task',
            'rows': '3',
            'style': 'margin-bottom: 20px'}))
        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Code of the task',
            'style': 'margin-bottom: 20px'}))


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your login',
        'style': 'margin-bottom: 20px'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'style': 'margin-bottom: 20px'
    }))


# Register form
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_staff']


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['code', 'name', 'description', 'responsible', 'initiator', 'priority', 'type', 'state',
                  'date_deadline']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Your code',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Your task name',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Your description',
            'style': 'margin-bottom: 20px'
        }))

        # self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
        #     'placeholder': 'Your description task',
        #     'style': 'margin-bottom: 20px'
        # }))

        # This line is correct for the modelChoiceField
        self.fields['responsible'].queryset = Employee.objects.filter(is_activate=True)
        self.fields['initiator'].queryset = Employee.objects.filter(is_activate=True)
        self.fields['priority'].queryset = Priority.objects.filter(is_activate=True)
        self.fields['type'].queryset = TypeTask.objects.filter(is_activate=True)
        self.fields['state'].queryset = State.objects.filter(is_activate=True)
        # self.fields['project'].queryset = Project.objects.filter(is_activate=True)

        self.fields['date_deadline'] = forms.CharField(widget=forms.DateInput(attrs={
            'placeholder': 'Deadline',
            'style': 'margin-bottom: 20px'
        }))


# This form provides employee creation
class CreateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['post', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['post'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Your post',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Bio',
            'style': 'margin-bottom: 20px'
        }))
