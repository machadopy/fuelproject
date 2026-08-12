from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from fuelrequests.forms import FuelReqForms
from fuelrequests.models import Fuelrequests
from fuelrequests.views.api import ReembolsosAPIV2list
from veiculos.models import Veiculo

import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status

from fuelrequests.models import Fuelrequests



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



User = get_user_model()


def _make_image_file(name='hodometro.jpg', fmt='JPEG'):
    """Gera uma imagem real (via Pillow) para passar tanto no ImageField
    quanto no FileExtensionValidator."""
    buffer = io.BytesIO()
    Image.new('RGB', (10, 10), color='red').save(buffer, format=fmt)
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type='image/jpeg')


class FuelrequestsAPIV2ViewsetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='machado', email='machado@test.com', password='123456'
        )
        self.other_user = User.objects.create_user(
            username='outro', email='outro@test.com', password='123456'
        )
        self.superuser = User.objects.create_superuser(
            username='admin', email='admin@test.com', password='123456'
        )

        self.veiculo = Veiculo.objects.create(
            placa='ABC1234', marca='Fiat', modelo='Palio', km=1000
        )

        self.list_url = '/fuelrequests/api/v2/'


    def _create_solicitacao(self, usuario, **kwargs):
        defaults = dict(km_inicial=100, km_final=200, veiculo=self.veiculo)
        defaults.update(kwargs)
        return Fuelrequests.objects.create(usuario=usuario, **defaults)

    def _detail_url(self, pk):
        return f'{self.list_url}{pk}/'

    # --- criação ---

    def test_create_reembolso_com_hodometro(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'km_inicial': 230,
            'km_final': 2000,
            'veiculo': self.veiculo.id,
            'hodometro': _make_image_file(),
        }
        response = self.client.post(self.list_url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        solicitacao = Fuelrequests.objects.get(id=response.data['id'])
        self.assertEqual(solicitacao.usuario, self.user)
        self.assertTrue(solicitacao.hodometro)

    def test_create_reembolso_sem_hodometro_e_opcional(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'km_inicial': 100,
            'km_final': 500,
            'veiculo': self.veiculo.id,
        }
        response = self.client.post(self.list_url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        solicitacao = Fuelrequests.objects.get(id=response.data['id'])
        self.assertFalse(solicitacao.hodometro)

    def test_create_com_extensao_invalida_e_rejeitado(self):
        self.client.force_authenticate(user=self.user)

        arquivo_invalido = SimpleUploadedFile(
            'documento.txt', b'conteudo qualquer', content_type='text/plain'
        )
        data = {
            'km_inicial': 100,
            'km_final': 500,
            'veiculo': self.veiculo.id,
            'hodometro': arquivo_invalido,
        }
        response = self.client.post(self.list_url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hodometro', response.data)

    def test_create_km_final_igual_km_inicial_e_invalido(self):
        self.client.force_authenticate(user=self.user)

        data = {'km_inicial': 100, 'km_final': 100, 'veiculo': self.veiculo.id}
        response = self.client.post(self.list_url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('km_final', response.data)

    def test_create_km_final_menor_que_km_inicial_e_invalido(self):
        self.client.force_authenticate(user=self.user)

        data = {'km_inicial': 500, 'km_final': 100, 'veiculo': self.veiculo.id}
        response = self.client.post(self.list_url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('km_final', response.data)

    def test_create_usuario_e_definido_automaticamente_pela_view(self):
        # garante que o usuario do request é usado mesmo se alguém tentar mandar outro
        self.client.force_authenticate(user=self.user)

        data = {'km_inicial': 100, 'km_final': 300, 'veiculo': self.veiculo.id}
        response = self.client.post(self.list_url, data, format='multipart')

        solicitacao = Fuelrequests.objects.get(id=response.data['id'])
        self.assertEqual(solicitacao.usuario, self.user)

    def test_create_sem_autenticacao_retorna_401(self):
        data = {'km_inicial': 100, 'km_final': 300, 'veiculo': self.veiculo.id}
        response = self.client.post(self.list_url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- listagem / paginação ---

    def test_list_pagination_page_size_is_twelve(self):
        self.client.force_authenticate(user=self.user)

        for i in range(13):
            self._create_solicitacao(self.user, km_inicial=i, km_final=i + 50)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 13)
        self.assertEqual(len(response.data['results']), 12)

        
    def test_usuario_comum_so_ve_suas_proprias_solicitacoes(self):
        minha = self._create_solicitacao(self.user)
        da_outra_pessoa = self._create_solicitacao(self.other_user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)

        ids_retornados = [item['id'] for item in response.data['results']]
        self.assertIn(minha.id, ids_retornados)
        self.assertNotIn(da_outra_pessoa.id, ids_retornados)

    def test_superuser_ve_solicitacoes_de_todos(self):
        self._create_solicitacao(self.user)
        self._create_solicitacao(self.other_user)

        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.list_url)

        self.assertEqual(response.data['count'], 2)

    def test_filtro_por_status(self):
        self._create_solicitacao(self.user, status='P')
        self._create_solicitacao(self.user, status='A')

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url, {'status': 'A'})

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['status'], 'A')

    def test_filtro_por_status_invalido_e_ignorado(self):
        self._create_solicitacao(self.user, status='P')

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url, {'status': 'X'})

        # status inválido não filtra nada, retorna tudo do usuário
        self.assertEqual(response.data['count'], 1)

    # --- retrieve / update / delete ---

    def test_usuario_nao_acessa_solicitacao_de_outro(self):
        da_outra_pessoa = self._create_solicitacao(self.other_user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._detail_url(da_outra_pessoa.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_acessa_solicitacao_de_qualquer_usuario(self):
        da_outra_pessoa = self._create_solicitacao(self.other_user)

        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self._detail_url(da_outra_pessoa.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_troca_imagem_do_hodometro(self):
        solicitacao = self._create_solicitacao(self.user, hodometro=_make_image_file('original.jpg'))
        imagem_antiga = solicitacao.hodometro.name

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self._detail_url(solicitacao.id),
            {'hodometro': _make_image_file('nova.jpg')},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        solicitacao.refresh_from_db()
        self.assertNotEqual(solicitacao.hodometro.name, imagem_antiga)

    def test_delete_remove_solicitacao(self):
        solicitacao = self._create_solicitacao(self.user)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self._detail_url(solicitacao.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Fuelrequests.objects.filter(id=solicitacao.id).exists())