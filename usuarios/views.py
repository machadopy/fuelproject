from django.shortcuts import redirect, render
from fuelrequests.models import Fuelrequests
from fuelrequests.forms import FuelReqForms


# Create your views here.
def usuarios(request):
        #solicitacoes = Fuelrequests.objects.all() ordenacao somente para teste
        solicitacoes = Fuelrequests.objects.all().order_by('-data_solicitacao')[:9]
        return render(request, 'usuarios/index.html', {'solicitacoes': solicitacoes})



def userlogin(request):
        return render(request, 'usuarios/userlogin.html')