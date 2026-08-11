from rest_framework import serializers
from veiculos.models import Veiculo
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from ..models import Usuario



class UsuariosSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    telefone = serializers.CharField()
    setor = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password and password2 is not None and password != password2:
                raise serializers.ValidationError(
                    {'As senhas devem ser iguais e não podem ser nulas.'})

        return attrs



    def save_email(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


    def save(self, **kwargs):
         return super().save(**kwargs)

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')

        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()

        return usuario
  
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


    def validate_email(self,value):
        email = value.strip().lower()


        if self.instance:
            qs = Usuario.objects.exclude(pk=self.instance.pk)
        else:
            qs = Usuario.objects.all()

        if qs.filter(email__iexact=email).exists():
            raise ValidationError('Já existe um usuário cadastrado com esse email.')

        return value

    def validate_username(self, value):
        if Usuario.objects.exclude(pk=self.instance.pk if self.instance else None).filter(username__iexact=value).exists():
            raise serializers.ValidationError('Já existe um usuário com esse username.')
        return value



class UsuarioSerializerMV(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'telefone',
            'setor',
            'password',
        ]

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')

        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()

        return usuario