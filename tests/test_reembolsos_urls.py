from django.test import TestCase
from django.urls import reverse


class ReembolsosURLsTest(TestCase):

    def test_recipe_search_url_is_correct(self):
        url = reverse('reembolsos:search')
        self.assertEqual(url, '/reembolsos/search/')

    def test_detalhes_reemsbolsos_url_is_correct(self):
        url = reverse('reembolsos:detalhes_reembolsos',args=(1,))
        self.assertEqual(url, '/reembolsos/1/')

