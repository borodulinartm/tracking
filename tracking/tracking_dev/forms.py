from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


# The form creation method. Another forms will create the same as this form.
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['code', 'name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите название',
                                                                            'style': 'margin-bottom: 20px'}))
        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs=
                                                                           {'placeholder': 'Введите описание',
                                                                            'rows': '3',
                                                                            'style': 'margin-bottom: 20px'}))
        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите код',
                                                                            'style': 'margin-bottom: 20px'}))

        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['code'].label = "Код"


# This class provides priority form
class CreatePriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['code', 'name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите название',
                                                                            'style': 'margin-bottom: 20px'}))
        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs=
                                                                           {'placeholder': 'Введите описание',
                                                                            'rows': '3',
                                                                            'style': 'margin-bottom: 20px'}))
        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите код',
                                                                            'style': 'margin-bottom: 20px'}))

        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['code'].label = "Код"


# This class allows users create a states form
class CreateStateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['code', 'name', 'description', 'isClosed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The view elements is a
        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите код',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите название',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Введите описание',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['isClosed'] = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
            'style': 'margin-bottom: 20px'
        }))

        # Enter the label of the fields
        self.fields['code'].label = "Код"
        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['isClosed'].label = "Состояние является конечным"


# This form provides enter the types of the task form
class CreateTypeTaskForm(forms.ModelForm):
    class Meta:
        model = TypeTask
        fields = ['code', 'name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите название',
            'style': 'margin-bottom: 20px'}))
        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Введите описание',
            'rows': '3',
            'style': 'margin-bottom: 20px'}))
        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите код',
            'style': 'margin-bottom: 20px'}))

        # Enter the label of the fields
        self.fields['code'].label = "Код"
        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ваш логин',
        'style': 'margin-bottom: 20px'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ваш пароль',
        'style': 'margin-bottom: 20px'
    }))


# Register form
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff']


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['code', 'name', 'description', 'responsible', 'initiator', 'priority', 'type', 'state',
                  'date_deadline']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите код',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите название',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Введите описание',
            'style': 'margin-bottom: 20px'
        }))

        # This line is correct for the modelChoiceField
        self.fields['responsible'].queryset = Employee.objects.filter(is_activate=True)
        self.fields['initiator'].queryset = Employee.objects.filter(is_activate=True)
        self.fields['priority'].queryset = Priority.objects.filter(is_activate=True)
        self.fields['type'].queryset = TypeTask.objects.filter(is_activate=True)
        self.fields['state'].queryset = State.objects.filter(is_activate=True)
        # self.fields['project'].queryset = Project.objects.filter(is_activate=True)

        self.fields['responsible'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }
        self.fields['initiator'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }
        self.fields['priority'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }
        self.fields['type'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }
        self.fields['state'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }

        self.fields['date_deadline'] = forms.DateField(widget=forms.SelectDateWidget(attrs={
            "style": "margin-bottom: 20px"
        }))

        # Enter the label to the all tasks
        self.fields['code'].label = "Код"
        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание задачи"
        self.fields['responsible'].label = "Отвественный"
        self.fields['initiator'].label = "Наблюдатель"
        self.fields['priority'].label = "Приоритет задачи"
        self.fields['type'].label = "Тип задачи"
        self.fields['state'].label = "Текущее состояние задачи"
        self.fields['date_deadline'].label = "Дата выполнения задания"


# This form provides employee creation
class CreateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['post', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['post'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Ваша должность',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Расскажите о себе',
            'style': 'margin-bottom: 20px'
        }))
