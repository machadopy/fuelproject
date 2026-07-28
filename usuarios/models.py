from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=False)
    setor = models.CharField(max_length=45, blank=True)
    bio =models.TextField(default="",blank=True)

    def clean_email(self):
        email = (self.email or '').strip().lower()

        if email and Usuario.objects.exclude(pk=self.pk).filter(email__iexact=email).exists():
            raise ValidationError('Já existe um usuário cadastrado com esse email.')

        return email

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

