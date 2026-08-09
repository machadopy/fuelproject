from django.contrib import messages
from django.shortcuts import redirect, render

from fuelrequests.forms import FuelReqForms
from fuelrequests.models import Fuelrequests
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='usuarios:user_login', redirect_field_name='next')

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
            messages.success(request, 'Solicitação de combustível criada com sucesso.')
            return redirect('usuarios:dashboard')
        
        else:

            solicitacao = Fuelrequests.objects.all()

            context = {
                'solicitacao' : solicitacao,
                'form' : form
                }

            messages.error(request, 'Não foi possível criar a solicitação. Verifique os campos do formulário.')

            return render(request, 'fuelrequests/fuelrequests.html', context)
