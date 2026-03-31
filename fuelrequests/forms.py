from django import forms
from .models import Fuelrequests

class FuelReqForms(forms.ModelForm):
    class Meta:
        model = Fuelrequests
        exclude = ('status',)