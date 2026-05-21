from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegisterForm(UserCreationForm):
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
