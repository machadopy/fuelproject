from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from usuarios.models import Usuario
from fuelrequests.models import Fuelrequests

class ProfileView(TemplateView):
    template_name = 'usuarios/profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')
        profile = get_object_or_404(Usuario, pk=profile_id)
        solicitacoes = Fuelrequests.objects.filter(usuario=profile).order_by('-data_solicitacao')[:9]

        return self.render_to_response({
            **context,
            'profile': profile,
            'page_solicitacoes': solicitacoes,
        })