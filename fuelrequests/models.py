from django.db import models
from django.conf import settings
from django.urls import reverse
from veiculos.models import Veiculo
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os

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

    def save(self, *args, **kwargs):
        if self.hodometro and not self.hodometro._committed:
            self.hodometro = self._compress_image(self.hodometro)

        if self.comprovante_fiscal and not self.comprovante_fiscal._committed:
            self.comprovante_fiscal = self._compress_image(self.comprovante_fiscal)

        super().save(*args, **kwargs)

    def _compress_image(self, image_field):
        # Pula PDFs, que não podem ser abertos pelo Pillow
        ext = os.path.splitext(image_field.name)[1].lower()
        if ext == '.pdf':
            return image_field

        try:
            img = Image.open(image_field)
        except Exception:
            # Se não conseguir abrir (arquivo corrompido, etc), mantém original
            return image_field

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        max_size = (1600, 1600)
        img.thumbnail(max_size, Image.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=70, optimize=True)
        buffer.seek(0)

        base_name = os.path.splitext(os.path.basename(image_field.name))[0]

        return InMemoryUploadedFile(
            buffer,
            'ImageField',
            f"{base_name}.jpg",
            'image/jpeg',
            sys.getsizeof(buffer),
            None
        )
    