from django.shortcuts import redirect, render
from fuelrequests.models import Fuelrequests
from fuelrequests.forms import FuelReqForms
from .models import Usuario


# Create your views here.
def usuarios(request):
        #solicitacoes = Fuelrequests.objects.all() ordenacao somente para teste
        solicitacoes = Fuelrequests.objects.all().order_by('-data_solicitacao')[:9]
        card_usuarios = Usuario.objects.all()

        context = {
                'solicitacoes': solicitacoes,
                'card_usuarios' : card_usuarios,
                'usuario_logado': request.user
        }

        return render(request, 'usuarios/index.html', context)



def userlogin(request):
        return render(request, 'usuarios/userlogin.html')




