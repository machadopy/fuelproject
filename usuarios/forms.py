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
