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
        response = self.client.get(reverse('reembolsos:search'))
        self.assertTemplateUsed(response, 'reembolsos/search.html')