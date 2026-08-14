from django.contrib import messages
from django.shortcuts import redirect, render

from fuelrequests.forms import FuelReqForms
from fuelrequests.models import Fuelrequests
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='usuarios:user_login', redirect_field_name='next')

@login_required(login_url='usuarios:user_login', redirect_field_name='next')
def fuelrequests(request):
    if request.method == 'GET':
        solicitacao = Fuelrequests.objects.all()
        form = FuelReqForms()

        context = {
            'solicitacao': solicitacao,
            'form': form
        }
        return render(request, 'fuelrequests/fuelrequests.html', context)
    
    elif request.method == 'POST':
        # NÃO SE ESQUEÇA de passar request.FILES caso haja upload da foto do hodômetro
        form = FuelReqForms(request.POST, request.FILES)
        
        if form.is_valid():
            # 1. Cria a instância na memória sem salvar no banco ainda
            nova_solicitacao = form.save(commit=False)
            
            # 2. Atribui o usuário logado à solicitação
            nova_solicitacao.usuario = request.user
            
            # 3. Agora sim, salva no banco de dados
            nova_solicitacao.save()
            
            messages.success(request, 'Solicitação de combustível criada com sucesso.')
            return redirect('usuarios:dashboard')
        
        else:
            solicitacao = Fuelrequests.objects.all()
            context = {
                'solicitacao': solicitacao,
                'form': form
            }
            messages.error(request, 'Não foi possível criar a solicitação. Verifique os campos do formulário.')
            return render(request, 'fuelrequests/fuelrequests.html', context)
