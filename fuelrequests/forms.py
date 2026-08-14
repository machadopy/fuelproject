from django import forms
from django.core.exceptions import ValidationError
from .models import Fuelrequests


class FuelReqForms(forms.ModelForm):
    """
    Formulário para ABRIR ou EDITAR a solicitação.
    O motorista INFORMA o KM inicial e o KM final.
    """
    class Meta:
        model = Fuelrequests
        # Excluímos apenas o que depende da ação do supervisor ou do recibo final
        exclude = ('status', 'usuario', 'supervisor_aprovador', 'comprovante_fiscal')

    def clean(self):
        cleaned_data = super().clean()
        km_inicial = cleaned_data.get('km_inicial')
        km_final = cleaned_data.get('km_final')

        # Validação do KM final em relação ao inicial
        if km_inicial is not None and km_final is not None:
            if km_final <= km_inicial:
                self.add_error(
                    'km_final', 
                    f'O KM final ({km_final}) deve ser maior que o KM inicial ({km_inicial}).'
                )

        # Trava: Solicitações que não estejam em PENDENTE não podem ter dados alterados
        if self.instance and self.instance.pk:
            if self.instance.status != Fuelrequests.StatusChoices.PENDENTE:
                raise ValidationError("Apenas solicitações com status 'PENDENTE' podem ser editadas.")

        return cleaned_data


class AnexarComprovanteForm(forms.ModelForm):
    """
    Formulário exclusivo para FECHAMENTO:
    Anexar o cupom fiscal / foto da nota após aprovação.
    """
    class Meta:
        model = Fuelrequests
        fields = ['comprovante_fiscal', 'hodometro']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comprovante_fiscal'].required = True