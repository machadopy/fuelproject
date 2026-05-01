from django.shortcuts import render
from fuelrequests.models import Fuelrequests
from django.shortcuts import get_object_or_404
from django.http import Http404



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


    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    reembolsos_list = Fuelrequests.objects.filter(
        status__icontains = search_term
    ).order_by('-data_solicitacao')

    return render(request, 'reembolsos/search.html',{
        'page_title': f'Pesquisa:"{search_term}',
        'solicitacoes': reembolsos_list,
    })




'''STATUS_CHOICES = [
        ('P', 'PENDENTE'),
        ('A', 'APROVADO'),
        ('N', 'NAO APROVADO'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    data_solicitacao = models.DateField(auto_now_add=True)
    '''