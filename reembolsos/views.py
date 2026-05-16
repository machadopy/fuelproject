from django.shortcuts import render
from fuelrequests.models import Fuelrequests
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination_function



def reembolsos(request):


    if request.user.is_superuser:
        solicitacoes = Fuelrequests.objects.all().order_by('-data_solicitacao')
    
    
    else:
        solicitacoes = Fuelrequests.objects.filter(usuario=request.user)

        solicitacoes = solicitacoes.order_by('-data_solicitacao')

    page_solicitacoes, pagination_range = make_pagination_function(request,solicitacoes, 6)

    return render(request, 'reembolsos/reembolsos.html', context={
            'page_solicitacoes':page_solicitacoes,
            'pagination_range': pagination_range
            })

def detalhes_reembolsos(request, id):

    solicitacao = get_object_or_404(Fuelrequests, id=id)

    context = {
            'solicitacoes' : [solicitacao]
            }


    return render(request, 'reembolsos/detalhes_reembolsos.html', context)


def search(request):

    if request.user.is_superuser:
        qs =  Fuelrequests.objects.all().order_by('-data_solicitacao')

    else:
        qs = Fuelrequests.objects.filter(usuario=request.user)

        qs = qs.order_by('-data_solicitacao')

    

    search_term = request.GET.get('q', '').strip()


    if not search_term:
        raise Http404()
    
    mapeamento = {
            'APROVADO': 'A',
            'PENDENTE': 'P',
            'NAO APROVADO': 'N',
            'NÃO APROVADO': 'N',
            'N APROVADO': 'N'
        }
    
    status_filtrar = mapeamento.get(search_term.upper(), search)
    
    
    reembolsos_list = qs.filter(
        Q(status__icontains = status_filtrar)|
        Q(usuario__username__icontains = search_term)).distinct().order_by('-data_solicitacao')
    
    reembolsos_list, pagination_range = make_pagination_function(request,reembolsos_list, 12)

    return render(request, 'reembolsos/search.html',{
        'page_title': f'Pesquisa:"{search_term}"',
        'page_solicitacoes': reembolsos_list,
        'pagination_range':pagination_range,
        'search_term' : search_term,
        'auq': f'&q={search_term}'
        
    })




'''STATUS_CHOICES = [
        ('P', 'PENDENTE'),
        ('A', 'APROVADO'),
        ('N', 'NAO APROVADO'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    data_solicitacao = models.DateField(auto_now_add=True)


     context = {
            'solicitacoes' : solicitacoes
            }

            


    '''