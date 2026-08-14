from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import Http404

from django.db.models import Q
from fuelrequests.models import Fuelrequests

from utils.pagination import make_pagination_function
from django.views.generic import ListView

from django.core.exceptions import PermissionDenied

from fuelrequests.forms import AnexarComprovanteForm




PER_PAGES = int(12)


 


class ReembolsosListViewBase(ListView):
    model = Fuelrequests
    paginate_by = None
    context_object_name = 'page_solicitacoes'
    ordering = ['-id']
    template_name = 'reembolsos/reembolsos.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).select_related('usuario', 'veiculo')

        if not self.request.user.is_superuser:
            qs = qs.filter(usuario=self.request.user)
        

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
        if not self.get_search_term():
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
        solicitacao = get_object_or_404(
            Fuelrequests.objects.filter(usuario=request.user),
            id=id,
        )

    if solicitacao.status != Fuelrequests.StatusChoices.PENDENTE:
        messages.error(
            request,
            'Esta solicitação já foi processada e não pode mais ser excluída.'
        )
        return redirect('reembolsos:detalhes_reembolsos', pk=solicitacao.id)

    solicitacao.delete()
    messages.success(request, 'Solicitação deletada com sucesso.')

    return redirect(reverse('usuarios:dashboard'))

def theory(request,*args, **kwargs):

    reembolsos = Fuelrequests.objects.all()

    print(reembolsos[0].usuario)

    context={'reembolsos':reembolsos}

    return render(
        request,
        'reembolsos/theory.html',
        context= context
    )


@login_required(login_url='usuarios:user_login')
def anexar_comprovante(request, pk):
    solicitacao = get_object_or_404(Fuelrequests, pk=pk)

    # Permissão: apenas o dono ou superusuário
    if solicitacao.usuario != request.user and not request.user.is_superuser:
        raise PermissionDenied("Você não tem permissão para alterar esta solicitação.")

    # Validação de Status: Apenas APROVADO ou APROVADO AGUARDANDO COMPROVANTE
    status_permitidos = [
        Fuelrequests.StatusChoices.APROVADO,
        Fuelrequests.StatusChoices.APROVADO_AGUARDANDO
    ]

    if solicitacao.status not in status_permitidos:
        messages.error(
            request, 
            f"Não é possível anexar comprovante para solicitação com status '{solicitacao.get_status_display()}'."
        )
        return redirect('fuelrequests:fuelrequests')

    if request.method == 'POST':
        form = AnexarComprovanteForm(request.POST, request.FILES, instance=solicitacao)
        if form.is_valid():
            obj = form.save(commit=False)
            # Ao anexar o comprovante, atualiza o status para CONCLUÍDO
            obj.status = Fuelrequests.StatusChoices.CONCLUIDO
            obj.save()
            
            messages.success(request, f"Comprovante da solicitação #{solicitacao.id} anexado com sucesso!")
            return redirect('reembolsos:detalhes_reembolsos', pk=solicitacao.id)
        else:
            messages.error(request, "Erro ao anexar comprovante. Verifique o arquivo e tente novamente.")
    else:
        form = AnexarComprovanteForm(instance=solicitacao)

    context = {
        'form': form,
        'solicitacao': solicitacao,
    }
    return render(request, 'reembolsos/anexar_comprovante.html', context)