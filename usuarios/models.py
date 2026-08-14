from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from veiculos.models import Veiculo


class Equipe(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Equipe")
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="equipes_supervisionadas",
        verbose_name="Supervisor Responsável"
    )

    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"

    def __str__(self):
        sup_nome = self.supervisor.get_full_name() or self.supervisor.username if self.supervisor else 'Sem Supervisor'
        return f"{self.nome} - Sup: {sup_nome}"


class Usuario(AbstractUser):
    class RoleChoices(models.TextChoices):
        ADMIN = 'ADM', 'Administrador / Gestor'
        SUPERVISOR = 'SUP', 'Supervisor'
        MOTORISTA = 'MOT', 'Motorista / Técnico'

    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=False)
    setor = models.CharField(max_length=45, blank=True)
    bio = models.TextField(default="", blank=True)

    # Novas colunas para Papel e Equipe
    role = models.CharField(
        max_length=3,
        choices=RoleChoices.choices,
        default=RoleChoices.MOTORISTA,
        verbose_name="Papel / Perfil"
    )
    equipe = models.ForeignKey(
        Equipe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="membros",
        verbose_name="Equipe Pertencente"
    )

    # Helper properties para facilitar verificações em views/templates
    @property
    def is_supervisor(self):
        return self.role == self.RoleChoices.SUPERVISOR or self.is_superuser

    @property
    def is_motorista(self):
        return self.role == self.RoleChoices.MOTORISTA

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
        return f"{self.username} ({self.get_role_display()})"