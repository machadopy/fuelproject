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
from django.views.generic import ListView


PER_PAGES = int(12)

class ReembolsosListViewBase(ListView):
    model = Fuelrequests
    paginate_by = None
    context_object_name = 'page_solicitacoes'
    ordering = ['-id']
    template_name = 'reembolsos/reembolsos.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return qs.order_by('-data_solicitacao')
        
        qs = qs.filter(usuario=self.request.user).order_by('-data_solicitacao')

        return qs
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)
        page_solicitacoes, pagination_range = make_pagination_function(
            self.request,
            context.get('page_solicitacoes'),
            PER_PAGES
            )

        context.update({
            'page_solicitacoes': page_solicitacoes,
            'pagination_range' : pagination_range
        })
        
        return context
    
class SearchListView(ReembolsosListViewBase):
    template_name = 'reembolsos/search.html'
    
    def get_search_term(self):
        return self.request.GET.get('q', '').strip()
    
    def dispatch(self, request, *args, **kwargs):
        if not self.get_search_term:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.get_search_term()

        mapeamento = {
            'APROVADO': 'A',
            'PENDENTE': 'P',
            'NAO APROVADO': 'N',
            'NÃO APROVADO': 'N',
            'N APROVADO': 'N'
        }
    
        status_filtrar = mapeamento.get(search_term.upper(), search_term)

        return qs.filter(
            Q(status__icontains=status_filtrar) |
            Q(usuario__username__icontains=search_term)
        ).distinct().order_by('-data_solicitacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.get_search_term()

        context.update({
            'page_title': f'Pesquisa: "{search_term}"',
            'search_term': search_term,
            'auq': f'&q={search_term}',
        })
        return context

 
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