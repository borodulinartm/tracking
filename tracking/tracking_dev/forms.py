from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, PasswordChangeForm, \
    UserChangeForm
from django.db.models import Q
from colorfield.widgets import ColorWidget

from .models import *


# The form creation method. Another forms will create the same as this form.
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['code', 'name', 'description', 'laboriousness', 'budget', 'date_deadline']

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
        self.fields['date_deadline'] = forms.DateField(widget=forms.DateInput())
        self.fields['laboriousness'] = forms.IntegerField(
            widget=forms.TextInput(attrs={'placeholder': 'Введите трудоёмкость',
                                          'style': 'margin-bottom: 20px'}))
        self.fields['budget'] = forms.IntegerField(
            widget=forms.TextInput(attrs={'placeholder': 'Введите бюджет проекта',
                                          'style': 'margin-bottom: 20px'}))

        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['code'].label = "Код"
        self.fields['date_deadline'].label = "Дата завершения проекта"
        self.fields['laboriousness'].label = "Трудоёмкость"
        self.fields['budget'].label = "Бюджет"

        self.fields['date_deadline'].help_text = "<p style='margin-bottom: 20px'>Формат ввода данных: гг-мм-дд. " \
                                                 "Пример: 2023-02-28</p>"


# This class provides priority form
class CreatePriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['code', 'name', 'description', 'priority_value', 'priority_color',
                  'projects']

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

        self.fields['priority_value'] = forms.IntegerField(widget=forms.NumberInput(attrs={
            'type': 'range',
            'class': 'form-range slider',
            'step': '1',
            'min': '1',
            'max': '100',
            'value': '1',
            'id': 'priority_value_ranger_mnu',
            'style': 'margin-bottom: 20px',
            'onInput': 'change_label_value()'
        }))

        self.fields['priority_color'] = forms.CharField(widget=forms.HiddenInput(), required=False)

        self.fields['projects'] = forms.ModelMultipleChoiceField(
            queryset=Project.objects.filter(is_activate=True),
            widget=forms.CheckboxSelectMultiple, required=False
        )

        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['code'].label = "Код"
        self.fields['priority_value'].label = "Значение приоритета (1)"
        self.fields['projects'].label = "Проекты"
        self.fields['priority_color'].label = "Цвет приоритета"


# This class allows users create a states form
class CreateStateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['code', 'name', 'description', 'percentage', 'isClosed', 'projects']

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

        self.fields['percentage'] = forms.IntegerField(error_messages={
            "invalid": "Введите числовое значение процента состояния"
        }, widget=forms.TextInput(attrs={
            'placeholder': 'Процент выполнения задачи при данном состоянии',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['isClosed'] = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
            'style': 'margin-bottom: 20px'
        }))

        self.fields['projects'] = forms.ModelMultipleChoiceField(
            queryset=Project.objects.filter(is_activate=True),
            widget=forms.CheckboxSelectMultiple, required=False
        )

        # Enter the label of the fields
        self.fields['code'].label = "Код"
        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['isClosed'].label = "Состояние является конечным"
        self.fields['percentage'].label = "Процент выполнения задачи"
        self.fields['projects'].label = "Проекты"


# This form provides enter the types of the task form
class CreateTypeTaskForm(forms.ModelForm):
    class Meta:
        model = TypeTask
        fields = ['code', 'name', 'description', 'projects']

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

        self.fields['projects'] = forms.ModelMultipleChoiceField(
            queryset=Project.objects.filter(is_activate=True),
            widget=forms.CheckboxSelectMultiple, required=False
        )

        # Enter the label of the fields
        self.fields['code'].label = "Код"
        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['projects'].label = "Проекты"


# This form provides sprint form
class CreateSprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['code', 'name', 'description', 'date_start', 'date_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите код',
            'style': 'margin-bottom: 20px'}))

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите название',
            'style': 'margin-bottom: 20px'}))

        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Введите описание',
            'rows': '3',
            'style': 'margin-bottom: 20px'}))

        self.fields['date_start'] = forms.DateField(widget=forms.DateInput())
        self.fields['date_end'] = forms.DateField(widget=forms.DateInput())

        self.fields['code'].label = "Код"
        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['date_start'].label = "Дата начала"
        self.fields['date_end'].label = "Дата окончания"

        self.fields['date_start'].help_text = "<p style='margin-bottom: 20px'>Формат ввода данных: гг-мм-дд. " \
                                              "Пример: 2023-02-28</p>"
        self.fields['date_end'].help_text = "<p style='margin-bottom: 20px'>Формат ввода данных: гг-мм-дд. " \
                                            "Пример: 2023-02-28</p>"


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
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        error_messages = {
            "username": {
                "required": "Данное поле является обязательным",
                "unique": "Пользователь с данным именем уже существует в системе"
            }
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }

        self.fields['last_name'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }

        self.fields['email'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }

        self.fields['username'].label = "Ник-нейм"
        self.fields['username'].help_text = "<p style='margin-bottom: 20px'>Обязательное поле. Длина ник-нейма " \
                                            "не больше 150 символов. " \
                                            "Допустимо использовать буквы, цифры, а также символы @/./+/-/_ </p>"

        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['email'].label = "Электронная почта"

        self.fields['password1'].label = "Пароль"
        self.fields['password1'].help_text = "<ul style='margin-bottom: 20px'><li>Ваш пароль не должен " \
                                             "совпадать с другой персональной информацией " \
                                             ".</li><li>Ваш пароль должен состоять минимум из 8 символов." \
                                             "</li><li>Нельзя использовать часто используемые пароли." \
                                             "</li><li>Ваш пароль должен содержать цифры, буквы.</li></ul>"

        self.fields['password2'].label = "Подтверждение пароля"
        self.fields['password2'].help_text = "<p style='margin-bottom: 20px'>Подтвердите Ваш " \
                                             "пароль для верификации в системе</p>"


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['code', 'name', 'description', 'responsible', 'initiator', 'manager', 'priority', 'type', 'state',
                  'date_deadline']

    def __init__(self, *args, **kwargs):
        assert 'initial' in kwargs and 'project' in kwargs['initial']
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
        self.fields['responsible'].queryset = Employee.objects.filter(Q(is_activate=True) &
                                                                      Q(projects=kwargs['initial']['project']))
        self.fields['initiator'].queryset = Employee.objects.filter(Q(is_activate=True) &
                                                                    Q(projects=kwargs['initial']['project']))
        self.fields['manager'].queryset = Employee.objects.filter(Q(is_activate=True) &
                                                                  Q(projects=kwargs['initial']['project']))
        self.fields['priority'].queryset = Priority.objects.filter(Q(is_activate=True) &
                                                                   Q(projects=kwargs['initial']['project']))
        self.fields['type'].queryset = TypeTask.objects.filter(Q(is_activate=True) &
                                                               Q(projects=kwargs['initial']['project']))
        self.fields['state'].queryset = State.objects.filter(Q(is_activate=True) &
                                                             Q(projects=kwargs['initial']['project']))

        self.fields['responsible'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }
        self.fields['initiator'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }
        self.fields['manager'].widget.attrs = {
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

        self.fields['date_deadline'] = forms.DateField(widget=forms.DateInput())

        # Enter the label to the all tasks
        self.fields['code'].label = "Код"
        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание задачи"
        self.fields['responsible'].label = "Отвественный"
        self.fields['initiator'].label = "Наблюдатель"
        self.fields['manager'].label = "Проверяющий"
        self.fields['priority'].label = "Приоритет задачи"
        self.fields['type'].label = "Тип задачи"
        self.fields['state'].label = "Текущее состояние задачи"
        self.fields['date_deadline'].label = "Дата выполнения задания"

        self.fields['date_deadline'].help_text = "<p style='margin-bottom: 20px'>Формат ввода данных: гг-мм-дд. " \
                                                 "Пример: 2023-02-28</p>"


# This form provides employee creation
class CreateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['profession', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['profession'].queryset = Profession.objects.filter(is_activate=True)
        self.fields['profession'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }

        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Расскажите о себе',
            'style': 'margin-bottom: 20px'
        }))

        self.fields['description'].label = "О себе"
        self.fields['profession'].label = "Профессия"


# Данная форма позволяет изменить пользовательские данные
class ChangeUserCustomForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Имя пользователя"
        self.fields['username'].help_text = "<p style='margin-bottom: 20px'>Обязательное поле. Длина ник-нейма " \
                                            "не больше 150 символов. " \
                                            "Допустимо использовать буквы, цифры, а также символы @/./+/-/_ </p>"

        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['email'].label = "Электронная почта"

        self.fields['first_name'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }

        self.fields['last_name'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }

        self.fields['email'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }

    def get_user_name(self):
        return self.fields['username']


class ChangePasswordCustomForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label="Старый пароль", widget=forms.PasswordInput(
        attrs={
            "style": "margin-bottom: 20px"
        }
    ), error_messages={"required": "Необходимо ввести старый пароль"})

    new_password1 = forms.CharField(required=True, label="Новый пароль", widget=forms.PasswordInput(
        attrs={
            "style": "margin-bottom: 20px"
        }
    ), error_messages={"required": "Необходимо ввести новый пароль"})

    new_password2 = forms.CharField(required=True, label="Подтвердите ввод нового пароля", widget=forms.PasswordInput(
        attrs={
            "style": "margin-bottom: 20px"
        }
    ), error_messages={"required": "Повторите ввод нового пароля"})

    error_messages = {
        'password_mismatch': 'Новые пароли не совпадают. Пожалуйста, повторите попытку'
    }

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                "Введённый пароль некорректен. Пожалуйста, попробуйте ввести пароль ещё раз",
                code='password_incorrect',
            )
        return old_password


# This form provides laboriousness form
class CreateLaboriousnessForm(forms.ModelForm):
    class Meta:
        model = Laboriousness
        fields = ['employee', 'capacity_plan', 'capacity_fact']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['employee'] = forms.ModelChoiceField(queryset=Employee.objects.all())

        self.fields['capacity_plan'] = forms.IntegerField(error_messages={
            "invalid": "Введите целое число"
        }, widget=forms.TextInput(attrs={
            'placeholder': 'Введите колчичество часов',
            'style': 'margin-bottom: 20px'
        }))
        self.fields['capacity_fact'] = forms.IntegerField(error_messages={
            "invalid": "Введите целое число"
        }, widget=forms.TextInput(attrs={
            'placeholder': 'Введите количество фактических часов',
            'style': 'margin-bottom: 20px'
        }))

        # Add the same style to the employee
        self.fields['employee'].label = "Сотрудник"
        self.fields['capacity_plan'].label = "Запланированное колчество часов"
        self.fields['capacity_fact'].label = "Фактическое количество часов"

        self.fields['employee'].widget.attrs = {
            "style": "margin-bottom: 20px"
        }

        # The capacity fact is non-required field
        self.fields['capacity_fact'].required = False


class CustomAuthenticationForm(LoginForm):
    username = UsernameField(label="Введите имя пользователя", widget=forms.TextInput(attrs={
        "auto_focus": True,
        "style": "margin-bottom: 20px;",
        "placeholder": "Ваш логин"
    }))

    password = forms.CharField(
        strip=False, label="Введите пароль",
        widget=forms.PasswordInput(attrs={
            "style": "margin-bottom: 20px",
            "placeholder": "Ваш пароль"
        })
    )


# Данная форма позволяет вводить должности
class ProfessionForm(forms.ModelForm):
    class Meta:
        model = Profession
        fields = ('code', 'name', 'description', 'salary')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={
            "placeholder": "Код профессии",
            "style": "margin-bottom: 20px"
        }))

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={
            "placeholder": "Название",
            "style": "margin-bottom: 20px"
        }))

        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={
            "placeholder": "Описание",
            "style": "margin-bottom: 20px"
        }))

        self.fields['salary'] = forms.IntegerField(widget=forms.TextInput(attrs={
            "placeholder": "Введите зарплату",
            "style": "margin-bottom: 20px"
        }))

        self.fields['code'].label = "Код"
        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
        self.fields['salary'].label = "Зарплата"
