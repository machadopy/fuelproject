from django.db import models
from django.conf import settings
from django.urls import reverse
from veiculos.models import Veiculo
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


# Create your models here.

class Fuelrequests(models.Model):
    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"
        ordering = ['-data_solicitacao', '-id']

    # TextChoices deixa o código mais limpo e pythonico
    class StatusChoices(models.TextChoices):
        PENDENTE = 'P', 'PENDENTE'
        APROVADO = 'A', 'APROVADO'
        APROVADO_AGUARDANDO = 'AG', 'APROVADO AGUARDANDO COMPROVANTE'
        NAO_APROVADO = 'N', 'NÃO APROVADO'
        CONCLUIDO = 'C', 'CONCLUÍDO / COM COMPROVANTE'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="solicitacoes",
        verbose_name="Motorista / Técnico"
    )
    supervisor_aprovador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitacoes_aprovadas",
        verbose_name="Supervisor Responsável"
    )
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        verbose_name="Veículo"
    )
    data_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Solicitação")

    km_inicial = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999999)
        ],
        blank=False,
        verbose_name="KM Inicial"
    )

    km_final = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999999)
        ],
        blank=True,
        null=True,
        verbose_name="KM Final"
    )

    status = models.CharField(
        max_length=2,  # Alterado para 2 caracteres por causa de 'AG'
        default=StatusChoices.PENDENTE,
        choices=StatusChoices.choices,
        verbose_name="Status"
    )

    hodometro = models.ImageField(
        upload_to='hodometros/%Y/%m/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        verbose_name='Foto do Hodômetro',
        blank=True,
        null=True
    )

    comprovante_fiscal = models.ImageField(
        upload_to='comprovantes/%Y/%m/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'pdf'])],
        verbose_name='Cupom / Nota Fiscal',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Solicitação #{self.id} - {self.usuario.username} [{self.get_status_display()}]'

    def clean(self):
        super().clean()

        if self.km_inicial is not None and self.km_final is not None:
            if self.km_final <= self.km_inicial:
                raise ValidationError({
                    'km_final': 'A quilometragem final deve ser maior do que a quilometragem inicial.'
                })

    @property
    def distancia_percorrida(self):
        if self.km_inicial is not None and self.km_final is not None:
            res = self.km_final - self.km_inicial
            return res if res > 0 else '!KM INVÁLIDO!'
        return 0

    def get_absolute_url(self):
        return reverse("reembolsos:detalhes_reembolsos", args=[self.id])