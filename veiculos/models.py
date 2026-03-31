from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.

class Veiculo(models.Model):
    placa = models.CharField(max_length=7, unique=True)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    km =  models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(999999)
    ],
    blank= False
    )
    

    def __str__(self):
        return f'{self.modelo} {self.placa}'