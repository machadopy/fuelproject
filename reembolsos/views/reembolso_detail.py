from django.views.generic import DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict

from .all import *

class ReembolsosDetail(DetailView):
    model = Fuelrequests
    context_object_name = 'page_solicitacao'
    template_name = 'reembolsos/detalhes_reembolsos.html'

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_superuser:
            return qs

        return qs.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitacoes'] = [self.object]
        return context



class ReembolsosDetailApiv1(ReembolsosDetail):
    def render_to_response(self, context, **response_kwargs):
        reembolsos = context['page_solicitacao']
        reembolsos_dict = model_to_dict(reembolsos)
        reembolsos_dict['veiculo'] = {
            'id': reembolsos.veiculo.id,
            'placa': reembolsos.veiculo.placa,
            'marca': reembolsos.veiculo.marca,
            'modelo': reembolsos.veiculo.modelo,
            'km': reembolsos.veiculo.km,
        }

        return JsonResponse(
            reembolsos_dict,
            safe=True
        )