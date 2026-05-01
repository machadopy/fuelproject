from django.test import TestCase
from django.urls import reverse


class ReembolsosURLsTest(TestCase):

    def test_recipe_search_url_is_correct(self):
        url = reverse('reembolsos:search')
        self.assertEqual(url, '/reembolsos/search/')