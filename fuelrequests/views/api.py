from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from ..models import Fuelrequests
from ..serializers import FuelrequestsSerializer

   
class ReembolsosApiV2Pagination(PageNumberPagination):
    page_size = 9


class ReembolsosApiv2Viewset(ModelViewSet):
    queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
    serializer_class = FuelrequestsSerializer
    pagination_class = ReembolsosApiV2Pagination


class ReembolsosAPIV2list(ListCreateAPIView):

    queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
    serializer_class = FuelrequestsSerializer
    pagination_class = ReembolsosApiV2Pagination

    def get_queryset(self):
        queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
        if not self.request.user.is_superuser:
            queryset = queryset.filter(usuario=self.request.user)
        return queryset.order_by('-id')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ReembolsosAPIV2detail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
    serializer_class = FuelrequestsSerializer
    pagination_class = ReembolsosApiV2Pagination

    def get_queryset(self):
        queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
        if not self.request.user.is_superuser:
            queryset = queryset.filter(usuario=self.request.user)
        return queryset.order_by('-id')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
