from django.views.generic import DetailView

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






