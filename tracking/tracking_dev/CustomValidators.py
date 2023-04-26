import functools
import gzip
import os
import re
from difflib import SequenceMatcher

from django.conf import settings
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.functional import lazy
from django.utils.html import format_html
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _, ngettext


class MinimumLengthValidator:
    """
    Validate whether the password is of a minimum length.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Ваш пароль недостаточного размера. Минимальное количество символов =  %(min_length)d.",
                    "Ваш пароль недостаточного размера. Минимальное количество символов =  %(min_length)d.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Ваш пароль недостаточного размера. Минимальное количество символов =  %(min_length)d.",
            "Ваш пароль недостаточного размера. Минимальное количество символов =  %(min_length)d.",
            self.min_length
        ) % {'min_length': self.min_length}


class CommonPasswordValidator:
    """
    Validate whether the password is a common password.

    The password is rejected if it occurs in a provided list, which may be gzipped.
    The list Django ships with contains 1000 common passwords, created by Mark Burnett:
    https://xato.net/passwords/more-top-worst-passwords/
    """
    DEFAULT_PASSWORD_LIST_PATH = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'common-passwords.txt.gz'
    )

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        try:
            with gzip.open(password_list_path) as f:
                common_passwords_lines = f.read().decode().splitlines()
        except IOError:
            with open(password_list_path) as f:
                common_passwords_lines = f.readlines()

        self.passwords = {p.strip() for p in common_passwords_lines}

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("Данный пароль часто используемый."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("Пароль не может быть часто используемым.")


class NumericPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Пароль не может состоять только из цифр."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Пароль не может состоять только из цифр.")