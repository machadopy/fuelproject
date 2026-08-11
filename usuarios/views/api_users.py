from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from fuelrequests.permissions import IsOwner

from fuelrequests.views.api import ReembolsosApiV2Pagination
from ..models import Usuario
from .serializers import UsuarioSerializerMV

class UsuarioApiV2ModelV(ModelViewSet):
    serializer_class = UsuarioSerializerMV
    pagination_class = ReembolsosApiV2Pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Usuario.objects.all()

        return Usuario.objects.filter(pk=self.request.user.pk)
