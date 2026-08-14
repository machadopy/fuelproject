from django.http import Http404
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from fuelrequests.models import Fuelrequests
from reembolsos.forms.reembolsos_form import ReembolsosEditForm

@method_decorator(
    login_required(
    login_url='usuarios:user_login',
    redirect_field_name='next'
    ),
    name='dispatch'
    )
class ReembolsoEdit(View):
    def __init__(self, *args, **kwargs):
         super().__init__(*args,**kwargs)


    def get_reembolso(self, id):
        if self.request.user.is_superuser:
            return get_object_or_404(Fuelrequests, id=id)

        return get_object_or_404(
            Fuelrequests.objects.filter(usuario=self.request.user), id=id
        )
            
            
    def render_reembolso(self,form):
        return render(
            self.request,
            'reembolsos/editar_reembolsos.html',
            context = {
                'form' : form,
                'reembolsos':form.instance
                })



    def get(self, request, id):
        
        reembolsos = self.get_reembolso(id)

        if reembolsos.status in ['A', 'N']:
                raise Http404("Solicitações aprovadas ou não aprovadas não podem ser editadas.")

        form = ReembolsosEditForm(instance = reembolsos)

        return self.render_reembolso(form)
        
        
    

    def post(self, request, id):
    
        reembolsos = self.get_reembolso(id)

        if reembolsos.status in ['A', 'N']:
                raise Http404("Solicitações aprovadas ou não aprovadas não podem ser editadas.")

        form = ReembolsosEditForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance = reembolsos
            )

    
        if form.is_valid():
            form.save()

            messages.success(request,'Formulario salvo!')
            

        return self.render_reembolso(form)
    

class ReembolsosDeleteView(ReembolsoEdit):

  def post(self, request, id):
    reembolsos = self.get_reembolso(id)

    # TRAVA DE SEGURANÇA: Permite deletar APENAS se estiver em 'P' (PENDENTE)
    # Qualquer outro status ('A', 'AG', 'N', 'C') impede a exclusão
    if (
        reembolsos.status != Fuelrequests.StatusChoices.PENDENTE
        and not request.user.is_superuser
    ):
      messages.error(
          request,
          'Esta solicitação já foi processada e não pode mais ser excluída.',
      )
      return redirect('reembolsos:detalhes_reembolsos', pk=reembolsos.id)

    reembolsos.delete()
    messages.success(request, 'Solicitação deletada com sucesso.')

    return redirect('usuarios:dashboard')