import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.core.exceptions import ValidationError

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

class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['password1'], 'placeholder', 'Senha:')
        add_attr(self.fields['password2'], 'placeholder', 'Confirme sua senha:')

        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Regex corrigido unificando as regras em uma única string válida
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')

        if password and not regex.match(password):
            raise ValidationError(
                "Senha deve ter: No mínimo 8 caracteres, letras maiúsculas, minúsculas e números. A senha e a confirmação devem ser iguais.",
                code='invalid'
            )
            
        return password


    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + (
            'email',
            'telefone',
            )


        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

        help_texts = {
            'username':''
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder':'Digite seu username. Ex:"user_name".'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder':'Digite seu email. Ex:"user@email.com".'
            }),
            'telefone': forms.NumberInput(attrs={
                'placeholder':'Digite seu telefone. Ex:"ddd 9 9999-9999".'
            })
        }