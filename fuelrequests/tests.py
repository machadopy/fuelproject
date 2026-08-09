from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from fuelrequests.forms import FuelReqForms
from fuelrequests.models import Fuelrequests
from fuelrequests.views.api import ReembolsosAPIV2list
from veiculos.models import Veiculo


class FuelReqFormsTests(TestCase):
    def test_tags_field_is_not_in_form(self):
        form = FuelReqForms()

        self.assertNotIn('tags', form.fields)


class FuelRequestAPITests(TestCase):
    def test_list_api_uses_project_page_size(self):
        user = get_user_model().objects.create_user(username='apiuser', password='123456')
        veiculo = Veiculo.objects.create(placa='ABC1234', marca='Ford', modelo='Focus', km=1000)

        for index in range(13):
            Fuelrequests.objects.create(
                usuario=user,
                veiculo=veiculo,
                km_inicial=1000 + index,
                km_final=1001 + index,
            )

        request = APIRequestFactory().get('/api/fuelrequests/')
        force_authenticate(request, user=user)

        response = ReembolsosAPIV2list.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 13)
        self.assertEqual(len(response.data['results']), 12)
