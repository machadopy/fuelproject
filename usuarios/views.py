from django.shortcuts import redirect, render
from fuelrequests.models import Fuelrequests
from fuelrequests.forms import FuelReqForms
from .models import Usuario
from django.core.paginator import Paginator


# Create your views here.
def usuarios(request):
        #solicitacoes = Fuelrequests.objects.all() ordenacao somente para teste
        card_usuarios = Usuario.objects.all()

        page_solicitacoes = Fuelrequests.objects.all().order_by('-data_solicitacao')[:9]
  
       
        return render(request, 'usuarios/index.html', {'page_solicitacoes':page_solicitacoes})




def userlogin(request):
        return render(request, 'usuarios/userlogin.html')




