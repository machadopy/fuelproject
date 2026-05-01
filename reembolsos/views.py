from django.shortcuts import render
from fuelrequests.models import Fuelrequests
from django.shortcuts import get_object_or_404



def reembolsos(request):

    if request.user.is_superuser:

        #solicitacoes = Fuelrequests.objects.all() ordenacao apenas p teste
        solicitacoes = Fuelrequests.objects.all().order_by('-data_solicitacao')

        context = {
            'solicitacoes' : solicitacoes
            }

        return render(request, 'reembolsos/reembolsos.html', context)
    
    else:
        solicitacoes = Fuelrequests.objects.filter(usuario=request.user)

        solicitacoes = solicitacoes.order_by('-data_solicitacao')
        
        context = {
            'solicitacoes' : solicitacoes
            }

        return render(request, 'reembolsos/reembolsos.html', context)
    

def detalhes_reembolsos(request, id):

    solicitacao = get_object_or_404(Fuelrequests, id=id)

    context = {
            'solicitacoes' : [solicitacao]
            }


    return render(request, 'reembolsos/detalhes_reembolsos.html', context)


def search(request):
    return render(request, 'reembolsos/search.html')
 