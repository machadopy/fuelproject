from django.core.exceptions import ValidationError
import re

def add_attr(field,attr_name,attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def strong_password(password):
    regex = re.compile(r'^?=.*[a-z]')(r'?=.*[A-Z]')(r'?=.*[0-9]{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Senha deve ter:'
            'No minimo 8 caracteres.'
            'Letra maiusculas, minusculas e numeros.'
        ),
            code='invalid'
        )
