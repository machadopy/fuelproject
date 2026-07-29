from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from usuarios import views
from django.contrib.auth import get_user_model
from fuelrequests.models import Fuelrequests
from veiculos.models import Veiculo

User = get_user_model()


class ProfileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='teste',
            email='teste@test.com',
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
                    email=f"{userdata['username']}@test.com",
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

    def test_profile_view_is_correct(self):
        url = reverse('usuarios:profile', args=(self.user.id,))
        resolved = resolve(url)
        self.assertIs(resolved.func.view_class, views.ProfileView)

    def test_profile_template_view_is_correct(self):
        self.client.login(username='teste', password='123')

        url = reverse('usuarios:profile', args=(self.user.id,))
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'usuarios/profile.html')

    def test_profile_returns_404_for_nonexistent_user(self):
        self.client.login(username='teste', password='123')

        url = reverse('usuarios:profile', args=(9999,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_profile_context_has_correct_user(self):
        self.client.login(username='teste', password='123')

        url = reverse('usuarios:profile', args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(response.context['profile'], self.user)

    def test_profile_shows_only_last_9_solicitacoes(self):
        for i in range(12):
            self.make_solicitacao(id=f'u{i}', slug=f'slug{i}', title=f'title{i}')

        self.client.login(username='teste', password='123')

        url = reverse('usuarios:profile', args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(len(response.context['page_solicitacoes']), 9)

    def test_profile_solicitacoes_ordered_by_most_recent(self):
        for i in range(5):
            self.make_solicitacao(id=f'u{i}', slug=f'slug{i}', title=f'title{i}')

        self.client.login(username='teste', password='123')

        url = reverse('usuarios:profile', args=(self.user.id,))
        response = self.client.get(url)

        datas = [item.data_solicitacao for item in response.context['page_solicitacoes']]
        self.assertEqual(datas, sorted(datas, reverse=True))

    def test_profile_does_not_show_other_user_requests(self):
        own_request = self.make_solicitacao(
            id=1,
            slug='own',
            title='own',
            userdata={'username': 'teste'},
        )
        other_request = self.make_solicitacao(
            id=2,
            slug='other',
            title='other',
            userdata={'username': 'admin'},
        )

        self.client.login(username='teste', password='123')

        url = reverse('usuarios:profile', args=(self.user.id,))
        response = self.client.get(url)

        self.assertIn(own_request, response.context['page_solicitacoes'])
        self.assertNotIn(other_request, response.context['page_solicitacoes'])

    def test_profile_with_no_solicitacoes_returns_empty_list(self):
        self.client.login(username='teste', password='123')

        url = reverse('usuarios:profile', args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_solicitacoes']), 0)

    def test_superuser_can_view_other_user_profile(self):
        self.client.login(username='admin', password='123')

        url = reverse('usuarios:profile', args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile'], self.user)