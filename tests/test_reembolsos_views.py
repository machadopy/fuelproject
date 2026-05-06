from django.test import TestCase
from django.urls import reverse, resolve
from reembolsos import views
from django.contrib.auth import get_user_model
from fuelrequests.models import Fuelrequests
from veiculos.models import Veiculo

User = get_user_model()

class ReembolsosViewsTest(TestCase):
    def setUp(self):
        # Criamos um usuário que será usado em todos os testes desta classe
        self.user = User.objects.create_user(
            username='teste',  # Se o seu model usar username, troque para username='teste'
            password='123'
        )
    
    def make_solicitacao(self, slug='test', title='Test', userdata=None, **kwargs):
        """
        Cria uma solicitação de combustível para testes.
        
        Args:
            slug: identificador único para a solicitação
            title: título/descrição da solicitação
            userdata: dicionário com dados do usuário (username, etc)
            **kwargs: argumentos adicionais para Fuelrequests
        
        Returns:
            Instância de Fuelrequests criada
        """
        # Usa dados do userdata se fornecido, caso contrário usa o usuário padrão
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
        
        # Cria um veículo para a solicitação
        veiculo, created = Veiculo.objects.get_or_create(
            placa=f'TST{slug[:4].upper()}',
            defaults={
                'marca': 'Teste',
                'modelo': title or 'Modelo Teste',
                'km': 10000
            }
        )
        
        # Define valores padrão para km_inicial e km_final
        km_inicial = kwargs.pop('km_inicial', 1000)
        km_final = kwargs.pop('km_final', km_inicial + 100)
        status = kwargs.pop('status', 'P')
        
        # Cria a solicitação
        solicitacao = Fuelrequests.objects.create(
            usuario=usuario,
            veiculo=veiculo,
            km_inicial=km_inicial,
            km_final=km_final,
            status=status,
            **kwargs
        )
        
        return solicitacao

    def test_reembolsos_search_view_is_correct(self):
        url = reverse('reembolsos:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_reembolsos_search_retuns_a_right_template(self):

        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='123'
        )
        self.client.login(username=superuser.username, password='123')

        response = self.client.get(reverse('reembolsos:search')+'?q=teste')
        self.assertTemplateUsed(response, 'reembolsos/search.html')

    def test_search_bar_returns_404_if_no_terms_write(self):

        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='123'
        )
        self.client.login(username=superuser.username, password='123')
        
        response = self.client.get(reverse('reembolsos:search'))
        self.assertEqual(response.status_code, 404)

    def test_search_term_is_on_page_and_scaped(self):

        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='123'
        )

        self.client.login(username=superuser.username, password='123')
        url = reverse('reembolsos:search') + '?q=<teste>'
        response = self.client.get(url)
        self.assertIn(
            'Pesquisa:&quot;&lt;teste&gt;',
            response.content.decode('utf-8'))
            
    def test_can_find_solicitacoes_by_status_choice(self):
        pass

    def test_can_find_solicitacoes_by_author(self):
        solicitacao1 = self.make_solicitacao(slug='one', title='one', userdata={'username': 'machado_vitor'})
        solicitacao2 = self.make_solicitacao(slug='two', title='two', userdata={'username': 'machado_m'})

        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='123'
        )
        self.client.login(username=superuser.username, password='123')

        search_url = reverse('reembolsos:search')
        response = self.client.get(f'{search_url}?q=machado')

        self.assertEqual(response.status_code, 200)
        self.assertIn(solicitacao1, response.context['page_solicitacoes'])
        self.assertIn(solicitacao2, response.context['page_solicitacoes'])

    def test_regular_user_cannot_see_other_user_request(self):


        solicitacao1 = self.make_solicitacao(slug = 'mine', title = 'mine', userdata={'username':'user_1'})

        solicitacao2 = self.make_solicitacao(slug = 'other', title = 'other', userdata={'username':'user_2'})

        self.client.login(username = 'user_1', password = '123')

        search_url = reverse('reembolsos:search')

        response = self.client.get(f'{search_url}?q=user')

        self.assertIn(solicitacao1, response.context['page_solicitacoes'])
        self.assertNotIn(solicitacao2, response.context['page_solicitacoes'])
        
    
    def test_super_user_can_see_other_user_request(self):


        solicitacao1 = self.make_solicitacao(
            slug = 'mine',                                              
            title = 'mine',
            userdata={'username':'user_1'})

        solicitacao2 = self.make_solicitacao(
            slug = 'other',
            title = 'other',
            userdata={'username':'user_2'})

        superuser = User.objects.create_superuser(
            username='admin_user',
            email='admin@test.com',
            password='123'
        )
        self.client.login(username=superuser.username, password='123')

        search_url = reverse('reembolsos:search')

        response = self.client.get(f'{search_url}?q=user')

        self.assertEqual(response.status_code, 200)
        self.assertIn(solicitacao1, response.context['page_solicitacoes'])
        self.assertIn(solicitacao2, response.context['page_solicitacoes'])
    
    

