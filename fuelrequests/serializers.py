from rest_framework import serializers
from veiculos.models import Veiculo
from .models import Fuelrequests


class FuelrequestsSerializer(serializers.Serializer):
    STATUS_CHOICES = [
        ('P', 'PENDENTE'),
        ('A', 'APROVADO'),
        ('N', 'NAO APROVADO'),
    ]

    id = serializers.IntegerField(read_only=True)
    km_inicial = serializers.IntegerField()
    km_final = serializers.IntegerField()

    usuario_name = serializers.StringRelatedField(source='usuario')
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)

    veiculo_name = serializers.StringRelatedField(source='veiculo')
    veiculo = serializers.PrimaryKeyRelatedField(queryset=Veiculo.objects.all())
    

    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='P')
    data_solicitacao = serializers.DateField(read_only=True)

    distancia = serializers.SerializerMethodField()

    hodometro = serializers.ImageField(required=False, allow_null=True)

    def get_distancia(self, obj):
        if isinstance(obj, dict):
            return None
        return f'{obj.distancia_percorrida} KM'

    def validate(self, attrs):
        km_inicial = attrs.get('km_inicial')
        km_final = attrs.get('km_final')

        if km_inicial is not None and km_final is not None:
            if km_inicial == km_final:
                raise serializers.ValidationError(
                    {'km_final': 'km_final não pode ser igual a km_inicial.'}
                )
            if km_final < km_inicial:
                raise serializers.ValidationError(
                    {'km_final': 'km_final não pode ser menor que km_inicial.'}
                )

        return attrs

    def validate_km_inicial(self, value):
        km_inicial = value

        if km_inicial < 0 or km_inicial > 999999:
            raise serializers.ValidationError('Valor da Kilometragem incorreto!')
        return value
    
    def validate_km_final(self, value):
            km_final = value
    
            if km_final < 0 or km_final > 999999:
                raise serializers.ValidationError('Valor da Kilometragem incorreto!')
            return value

    def save(self, **kwargs):
         return super().save(**kwargs)

    def create(self, validated_data):
        return Fuelrequests.objects.create(**validated_data, usuario=self.context['request'].user)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class FuelrequestsSerializerV3(serializers.ModelSerializer):
    class Meta:
        model = Fuelrequests
        fields = [
            'id',
            'km_inicial',
            'km_final',
            'distancia',
            'hodometro',
        ]

    distancia = serializers.SerializerMethodField()

    def get_distancia(self, obj):
        return f'{obj.distancia_percorrida} KM'

