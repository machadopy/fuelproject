from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView

from tag.models import Tag
from ..serializers import TagSerializer

from ..models import Fuelrequests
from ..serializers import FuelrequestsSerializer #, FuelrequestsSerializerV3

class ReembolsosAPIV2list(ListCreateAPIView):

    queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
    serializer_class = FuelrequestsSerializer

    def get_queryset(self):
        queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
        if not self.request.user.is_superuser:
            queryset = queryset.filter(usuario=self.request.user)
        return queryset.order_by('-id')[:10]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

'''    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
        
        if not request.user.is_superuser:
            queryset = queryset.filter(usuario=request.user)

        reembolsos = queryset.order_by('-id')[:10]
        serializer = FuelrequestsSerializer(instance=reembolsos, many=True, context={'request': request})

        return Response(serializer.data)


    def post(self,request):
        serializer = FuelrequestsSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(usuario=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)'''


class ReembolsosAPIV2detail(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')
        if not request.user.is_superuser:
            queryset = queryset.filter(usuario=request.user)
        return queryset

    def get(self,request,pk):
        queryset = self.get_queryset(request)

        reembolso = get_object_or_404(queryset, pk=pk)    
    
        
        serializer = FuelrequestsSerializer(
            instance=reembolso,
            context={'request': request}
        )
            
        return Response(serializer.data)

        
    def patch(self, request,pk):
        queryset = self.get_queryset(request)

        reembolso = get_object_or_404(queryset, pk=pk)    

        serializer = FuelrequestsSerializer(
            instance=reembolso,
            data=request.data,
            partial=True,
            context={'request': request}
        )
                
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,)

    def delete(self,request,pk):
        queryset = self.get_queryset(request)
        reembolso = get_object_or_404(queryset, pk=pk)    

        reembolso.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tag_api_detail(request, pk):
    queryset = Tag.objects.all()

    if not request.user.is_superuser:
        queryset = queryset.filter(usuario=request.user)

    tag = get_object_or_404(queryset, pk=pk)
    
    serializer = TagSerializer(instance=tag, context={'request': request})
    return Response(serializer.data)



'''@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def reembolsos_listv3(request):
    # Base do QuerySet otimizada com JOIN para usuario e veiculo
    queryset = Fuelrequests.objects.select_related('usuario', 'veiculo')

    # Regra de acesso: Superusuario vê tudo, usuário comum vê só o dele
    if not request.user.is_superuser:
        queryset = queryset.filter(usuario=request.user)

    reembolsos = queryset.order_by('-id')[:10]
    serializer = FuelrequestsSerializerV3(instance=reembolsos, many=True,context={'request': request})
    return Response(serializer.data)'''
