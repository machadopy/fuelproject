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
        
    STATUS_CHOICES = [
        ('P', 'PENDENTE'),
        ('A', 'APROVADO'),
        ('N', 'NAO APROVADO'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    data_solicitacao = models.DateField(auto_now_add=True)
    
    km_inicial = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(999999)
    ],
    blank= False,
    )


    km_final = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(999999)
    ],
    blank= False,
    )

    status = models.CharField(max_length=1, default='P', choices=STATUS_CHOICES)

    hodometro = models.ImageField(
        upload_to='hodometros/%Y/%m/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        verbose_name='Foto do Hodômetro',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Solicitacao {self.id} - {self.usuario.username}'

    def clean(self):
        super().clean()

        if self.km_inicial is not None and self.km_final is not None:
            if self.km_final <= self.km_inicial:
                raise ValidationError({
                    'km_final': 'A quilometragem final deve ser maior do que a quilometragem inicial.'
                })
    
    @property
    def distancia_percorrida(self):
        res = 0
        if self.km_inicial and self.km_final:
            res = self.km_final-self.km_inicial

            if res <= 0:
                return '!KM INVALIDO!'
            else:
                return res 
                
        return 0
    
    def get_absolute_url(self):
        return reverse("reembolsos:detalhes_reembolsos", args={self.id})