from django.test import TestCase
from django.urls import reverse, resolve
from reembolsos import views
from django.contrib.auth import get_user_model

User = get_user_model()

class ReembolsosViewsTest(TestCase):
    def setUp(self):
        # Criamos um usuário que será usado em todos os testes desta classe
        self.user = User.objects.create_user(
            username='teste',  # Se o seu model usar username, troque para username='teste'
            password='123'
        )

    def test_reembolsos_search_view_is_correct(self):
        url = reverse('reembolsos:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_reembolsos_search_retuns_a_right_template(self):
        response = self.client.get(reverse('reembolsos:search')+'?q=teste')
        self.assertTemplateUsed(response, 'reembolsos/search.html')

    def test_search_bar_returns_404_if_no_terms_write(self):
        response = self.client.get(reverse('reembolsos:search'))
        self.assertEqual(response.status_code, 404)

    def test_search_term_is_on_page_and_scaped(self):
        url = reverse('reembolsos:search') + '?q=<teste>'
        response = self.client.get(url)
        self.assertIn(
            'Pesquisa:&quot;&lt;teste&gt;',
            response.content.decode('utf-8'))
            