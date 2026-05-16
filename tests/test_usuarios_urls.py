from django.test import TestCase
from django.urls import reverse

class UsuariosUrlsTest(TestCase):

    def test_if_user_url_are_correct(self):
        url = reverse('usuarios:user_page')
        self.assertEqual(url, '/')

    def test_if_user_login_url_are_correct(self):
        url = reverse('usuarios:user_login')
        self.assertEqual(url,'/user_login/')

    