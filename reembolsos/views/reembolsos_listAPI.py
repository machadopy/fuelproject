from .all import *
from django.http import JsonResponse


class ReembolsosListApiv1(ReembolsosListViewBase):
    template_name = 'reembolsos/reembolsos.html'

    def render_to_response(self, context, **response_kwargs):
        reembolsos = context['page_solicitacoes']
        reembolsos_dict = list(reembolsos.object_list.values())

        return JsonResponse({
            'results': reembolsos_dict,
            'count': reembolsos.paginator.count,
            'page': reembolsos.number,
            'num_pages': reembolsos.paginator.num_pages,
        }, **response_kwargs)





    