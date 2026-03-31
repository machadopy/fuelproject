from django.shortcuts import redirect, render

from fuelrequests.forms import FuelReqForms
from fuelrequests.models import Fuelrequests

# Create your views here.
def fuelrequests(request):
# Create your views here.
    if request.method == 'GET':

        solicitacao = Fuelrequests.objects.all()

        form = FuelReqForms()

        context = {
            'solicitacao' : solicitacao,
            'form' : form
        }

        return render(request, 'fuelrequests/fuelrequests.html', context)
    
    elif request.method == 'POST':
        
        form = FuelReqForms(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('/')
        
        else:

            solicitacao = Fuelrequests.objects.all()

            context = {
                'solicitacao' : solicitacao,
                'form' : form
                }

            return render(request, 'fuelrequests/fuelrequests.html', context)
