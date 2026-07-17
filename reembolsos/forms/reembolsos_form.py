from django import forms
from fuelrequests.models import Fuelrequests

class ReembolsosEditForm(forms.ModelForm):
    
    class Meta:
        model = Fuelrequests
        fields = ('km_inicial', 'km_final')
