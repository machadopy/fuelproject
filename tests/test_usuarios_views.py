from django.test import TestCase
from django.urls import reverse, resolve
from reembolsos import views
from django.contrib.auth import get_user_model
from fuelrequests.models import Fuelrequests
from veiculos.models import Veiculo
from django.contrib.auth.models import User

User = get_user_model()

class UsuariosViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teste',
            password='123'
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='123'        
        )
    
    def make_solicitacao(self, id, slug='test', title='Test', userdata=None, **kwargs):

        if userdata and 'username' in userdata:
            try:
                usuario = User.objects.get(username=userdata['username'])
            except User.DoesNotExist:
                usuario = User.objects.create_user(
                    username=userdata['username'],
                    password='123'
                )
        else:
            usuario = self.user
        
        veiculo, created = Veiculo.objects.get_or_create(
            placa=f'TST{slug[:4].upper()}',
            defaults={
                'marca': 'Teste',
                'modelo': title or 'Modelo Teste',
                'km': 10000
            }
        )
        
        km_inicial = kwargs.pop('km_inicial', 1000)
        km_final = kwargs.pop('km_final', km_inicial + 100)
        status = kwargs.pop('status', 'P')
        
        solicitacao = Fuelrequests.objects.create(
            usuario=usuario,
            veiculo=veiculo,
            km_inicial=km_inicial,
            km_final=km_final,
            status=status,
            **kwargs
        )
        
        return solicitacao
  

    def test_usuarios_template_view_is_correct(self):
 
        self.client.login(username='teste', password='123')

        url = reverse('usuarios:user_page')


        response = self.client.get(url)
        self.assertTemplateUsed(response, 'usuarios/index.html')

    
    def test_usuarios_login_template_view_is_correct(self):
 
        self.client.login(username='teste', password='123')

        url = reverse('usuarios:user_login')


        response = self.client.get(url)
        self.assertTemplateUsed(response, 'usuarios/user_login.html')