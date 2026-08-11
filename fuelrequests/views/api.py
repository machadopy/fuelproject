from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ..models import Fuelrequests
from ..serializers import FuelrequestsSerializer
from ..permissions import IsOwner

   
class ReembolsosApiV2Pagination(PageNumberPagination):
    page_size = 9


class ReembolsosApiv2Viewset(ModelViewSet):
    queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
    serializer_class = FuelrequestsSerializer
    pagination_class = ReembolsosApiV2Pagination
    permission_classes = [IsAuthenticated, IsOwner]


    def get_queryset(self):
        qs = super().get_queryset()
        status_id = self.request.query_params.get('status', None)

        if not self.request.user.is_superuser:
            qs = qs.filter(usuario_id=self.request.user.id)

        status_valido = [st[0] for st in FuelrequestsSerializer.STATUS_CHOICES]
        if status_id is not None and status_id in status_valido:
            qs = qs.filter(status=status_id)

        
        return qs

    def get_object(self):
        pk = self.kwargs.get('pk','')
        obj = get_object_or_404(self.get_queryset(), pk=pk,)

        self.check_object_permissions(self.request, obj)

        return obj

    

class ReembolsosAPIV2list(ListCreateAPIView):

    queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
    serializer_class = FuelrequestsSerializer
    pagination_class = ReembolsosApiV2Pagination
    permission_classes = [IsAuthenticated, IsOwner]
    http_method_names = ['get', 'options', 'head', 'patch', 'post', 'delete']

    def get_queryset(self):
        queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
        if not self.request.user.is_superuser:
            queryset = queryset.filter(usuario_id=self.request.user.id)
        return queryset.order_by('-id')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ReembolsosAPIV2detail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
    serializer_class = FuelrequestsSerializer
    pagination_class = ReembolsosApiV2Pagination

    def get_queryset(self):
        queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
        if not self.request.user.is_superuser:
            queryset = queryset.filter(usuario_id=self.request.user.id)
        return queryset.order_by('-id')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
