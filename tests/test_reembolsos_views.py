from django.test import TestCase
from django.urls import reverse, resolve
from reembolsos import views
from django.contrib.auth import get_user_model
from fuelrequests.models import Fuelrequests
from veiculos.models import Veiculo
from django.contrib.auth.models import User

User = get_user_model()

class ReembolsosViewsTest(TestCase):
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
    
    def test_reembolsos_template_view_is_correct(self):

        self.client.login(username='teste', password='123')

        url = reverse('reembolsos:reembolsos_all')


        response = self.client.get(url)
        self.assertTemplateUsed(response, 'reembolsos/reembolsos.html')

    def test_detalhes_reembolsos_template_view_is_correct(self):

        solicitacao = self.make_solicitacao(1)

        self.client.login(username='admin', password='123')

        url = reverse('reembolsos:detalhes_reembolsos',args=(solicitacao.id,))
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'reembolsos/detalhes_reembolsos.html')

    def test_reembolsos_search_view_is_correct(self):

        url = reverse('reembolsos:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_reembolsos_search_retuns_a_right_template(self):
        
        self.client.login(username='admin', password='123')

        response = self.client.get(reverse('reembolsos:search')+'?q=teste')
        self.assertTemplateUsed(response, 'reembolsos/search.html')

    def test_search_bar_returns_404_if_no_terms_write(self):

        self.client.login(username='admin', password='123')
        
        response = self.client.get(reverse('reembolsos:search'))
        self.assertEqual(response.status_code, 404)

    def test_search_term_is_on_page_and_scaped(self):

        self.client.login(username='admin', password='123')
        url = reverse('reembolsos:search') + '?q=<teste>'
        response = self.client.get(url)
        self.assertIn(
            'Pesquisa:&quot;&lt;teste&gt;',
            response.content.decode('utf-8'))
            
    def test_can_find_solicitacoes_by_status_choice(self):
        pass

    def test_can_find_solicitacoes_by_author(self):
        solicitacao1 = self.make_solicitacao(id=2, slug='one', title='one', userdata={'username': 'machado_vitor'})
        solicitacao2 = self.make_solicitacao(id =3, slug='two', title='two', userdata={'username': 'machado_m'})

        self.client.login(username='admin', password='123')

        search_url = reverse('reembolsos:search')
        response = self.client.get(f'{search_url}?q=machado')

        self.assertEqual(response.status_code, 200)
        self.assertIn(solicitacao1, response.context['page_solicitacoes'])
        self.assertIn(solicitacao2, response.context['page_solicitacoes'])

    def test_regular_user_cannot_see_other_user_request(self):


        solicitacao1 = self.make_solicitacao(id=2,slug = 'mine', title = 'mine', userdata={'username':'user_1'})

        solicitacao2 = self.make_solicitacao(id=3,slug = 'other', title = 'other', userdata={'username':'user_2'})

        self.client.login(username = 'user_1', password = '123')

        search_url = reverse('reembolsos:search')

        response = self.client.get(f'{search_url}?q=user')

        self.assertIn(solicitacao1, response.context['page_solicitacoes'])
        self.assertNotIn(solicitacao2, response.context['page_solicitacoes'])
        
    
    def test_super_user_can_see_other_user_request(self):


        solicitacao1 = self.make_solicitacao(
            id=2,
            slug = 'mine',                                              
            title = 'mine',
            userdata={'username':'user_1'})

        solicitacao2 = self.make_solicitacao(
            id=3,
            slug = 'other',
            title = 'other',
            userdata={'username':'user_2'})

        self.client.login(username='admin', password='123')

        search_url = reverse('reembolsos:search')

        response = self.client.get(f'{search_url}?q=user')

        self.assertEqual(response.status_code, 200)
        self.assertIn(solicitacao1, response.context['page_solicitacoes'])
        self.assertIn(solicitacao2, response.context['page_solicitacoes'])
    
    

