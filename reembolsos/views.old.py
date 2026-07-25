from django.contrib import messages

from django.shortcuts import redirect, render
from django.urls import reverse
from fuelrequests.models import Fuelrequests
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from reembolsos.forms.reembolsos_form import ReembolsosEditForm
from utils.pagination import make_pagination_function
from django.contrib.auth.decorators import login_required


PER_PAGES = int(12)

@login_required(login_url='usuarios:user_login', redirect_field_name='next')

def reembolsos(request):


    if request.user.is_superuser:
        solicitacoes = Fuelrequests.objects.all().order_by('-data_solicitacao')
    
    
    else:
        solicitacoes = Fuelrequests.objects.filter(usuario=request.user)

        solicitacoes = solicitacoes.order_by('-data_solicitacao')

    page_solicitacoes, pagination_range = make_pagination_function(request,solicitacoes, PER_PAGES)

    return render(request, 'reembolsos/reembolsos.html', context={
            'page_solicitacoes':page_solicitacoes,
            'pagination_range': pagination_range
            })
@login_required(login_url='usuarios:user_login', redirect_field_name='next')
def detalhes_reembolsos(request, id):

    if request.user.is_superuser:
        solicitacao = get_object_or_404(Fuelrequests, id=id)

    else:
        solicitacao = get_object_or_404(Fuelrequests.objects.filter(usuario=request.user), id=id)

    context = {
            'solicitacoes' : [solicitacao]
            }
    

    return render(request, 'reembolsos/detalhes_reembolsos.html', context)

@login_required(login_url='usuarios:user_login', redirect_field_name='next')
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
    
    reembolsos_list, pagination_range = make_pagination_function(request,reembolsos_list, PER_PAGES)

    return render(request, 'reembolsos/search.html',{
        'page_title': f'Pesquisa:"{search_term}"',
        'page_solicitacoes': reembolsos_list,
        'pagination_range':pagination_range,
        'search_term' : search_term,
        'auq': f'&q={search_term}'
        
    })

@login_required(login_url='usuarios:user_login', redirect_field_name='next')
def editar_reembolsos(request, id):
    

    if request.user.is_superuser:
        solicitacao = get_object_or_404(Fuelrequests, id=id)

    else:
        solicitacao = get_object_or_404(Fuelrequests.objects.filter(
            usuario=request.user),
            id=id,
            )
        if solicitacao.status in ['A', 'N']:
            raise Http404("Solicitações aprovadas ou não aprovadas não podem ser editadas.")

    form = ReembolsosEditForm(
    data=request.POST or None,
    files=request.FILES or None,
    instance = solicitacao
    )

    context = {
            'solicitacoes' : [solicitacao],
            'form' : form
            }
    if form.is_valid():
        solicitacao = form.save()

        messages.success(request,'Formulario salvo!')
        

    return render(request, 'reembolsos/editar_reembolsos.html', context)


@login_required(login_url='usuarios:user_login', redirect_field_name='next')
def deletar_reembolsos(request, id):
    if request.method != 'POST':
        raise Http404()

    if request.user.is_superuser:
        solicitacao = get_object_or_404(Fuelrequests, id=id)

    else:
        solicitacao = get_object_or_404(Fuelrequests.objects.filter(
            usuario=request.user),
            id=id,
            )
        if solicitacao.status in ['A', 'N']:
            raise Http404("Solicitações aprovadas ou não aprovadas não podem ser deletadas.")

    solicitacao.delete()
    messages.success(request, 'Solicitação deletada com sucesso.')

    return redirect(reverse('usuarios:dashboard'))