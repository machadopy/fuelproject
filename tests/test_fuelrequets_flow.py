from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from fuelrequests.forms import AnexarComprovanteForm
from fuelrequests.models import Fuelrequests
from usuarios.models import Equipe
from veiculos.models import Veiculo

import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

Usuario = get_user_model()


class FuelProjectFlowTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        # 1. Criação de Usuários com Perfil / Role
        self.supervisor = Usuario.objects.create_user(
            username='supervisor_test',
            email='sup@test.com',
            password='password123',
            role=Usuario.RoleChoices.SUPERVISOR
        )

        self.equipe = Equipe.objects.create(
            nome="Equipe Alpha",
            supervisor=self.supervisor
        )

        self.motorista = Usuario.objects.create_user(
            username='motorista_test',
            email='mot@test.com',
            password='password123',
            role=Usuario.RoleChoices.MOTORISTA,
            equipe=self.equipe
        )

        self.admin = Usuario.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='password123',
            role=Usuario.RoleChoices.ADMIN
        )

        # 2. Criação de Veículo
        # 2. Criação de Veículo
        self.veiculo = Veiculo.objects.create(
            modelo="Uno Mille",
            placa="ABC1234",
            km=10000  # Adicionada quilometragem obrigatória
        )

        # 3. Imagem válida para uploads
        image_file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='blue')
        image.save(image_file, 'jpeg')
        image_file.seek(0)

        self.fake_image = SimpleUploadedFile(
            name='comprovante.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )

    # ==========================================
    # TESTES DE MODEL & VALIDATION
    # ==========================================

    def test_distancia_percorrida_calculation(self):
        """Valida o cálculo do property distancia_percorrida."""
        solicitacao = Fuelrequests.objects.create(
            usuario=self.motorista,
            veiculo=self.veiculo,
            km_inicial=1000,
            km_final=1150
        )
        self.assertEqual(solicitacao.distancia_percorrida, 150)

    # ==========================================
    # TESTES DE FORMS
    # ==========================================



# ... dentro do seu teste ...

    def test_anexar_comprovante_form_validation(self):
        """Form de comprovante deve ser válido quando arquivo é enviado."""
        
        # 1. Cria uma imagem real válida em memória para passar pelo Pillow/ImageField
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'jpeg')
        file.seek(0)
        
        fake_jpg = SimpleUploadedFile(
            name='comprovante.jpg',
            content=file.read(),
            content_type='image/jpeg'
        )

        solicitacao = Fuelrequests.objects.create(
            usuario=self.motorista,
            veiculo=self.veiculo,
            km_inicial=1000
        )

        # 2. Garante que os campos de dados do POST batem com o que o clean do Form exige
        form_data = {
            'km_inicial': 1000,
            'km_final': 1200
        }
        file_data = {
            'comprovante_fiscal': fake_jpg
        }

        form = AnexarComprovanteForm(data=form_data, files=file_data, instance=solicitacao)
        
        # Se ainda assim falhar, isso printa o erro exato do form no terminal
        if not form.is_valid():
            print("\nERROS DO FORMULARIO:", form.errors)

        self.assertTrue(form.is_valid())

    # ==========================================
    # TESTES DE VIEWS & BLOQUEIOS DE STATUS
    # ==========================================

    def test_bloqueio_edicao_quando_nao_pendente(self):
        """NENHUM usuário (nem admin) pode editar solicitação fora do status PENDENTE."""
        solicitacao = Fuelrequests.objects.create(
            usuario=self.motorista,
            veiculo=self.veiculo,
            km_inicial=1000,
            km_final=1200,
            status=Fuelrequests.StatusChoices.APROVADO_AGUARDANDO
        )

        # Tenta editar como Admin
        self.client.login(username='admin_test', password='password123')
        url = reverse('reembolsos:editar_reembolsos', kwargs={'id': solicitacao.id})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Deve redirecionar bloqueando

    def test_bloqueio_delecao_quando_nao_pendente(self):
        """NENHUM usuário (nem admin) pode deletar solicitação fora do status PENDENTE."""
        solicitacao = Fuelrequests.objects.create(
            usuario=self.motorista,
            veiculo=self.veiculo,
            km_inicial=1000,
            km_final=1200,
            status=Fuelrequests.StatusChoices.CONCLUIDO
        )

        # Tenta deletar como Admin
        self.client.login(username='admin_test', password='password123')
        url = reverse('reembolsos:deletar_reembolsos', kwargs={'id': solicitacao.id})
        
        response = self.client.post(url)
        
        # Garante que o registro AINDA existe no banco
        self.assertTrue(Fuelrequests.objects.filter(id=solicitacao.id).exists())
        self.assertEqual(response.status_code, 302)

    def test_sucesso_delecao_quando_pendente(self):
        """Solicitação com status PENDENTE pode ser deletada."""
        solicitacao = Fuelrequests.objects.create(
            usuario=self.motorista,
            veiculo=self.veiculo,
            km_inicial=1000,
            status=Fuelrequests.StatusChoices.PENDENTE
        )

        self.client.login(username='motorista_test', password='password123')
        url = reverse('reembolsos:deletar_reembolsos', kwargs={'id': solicitacao.id})
        
        response = self.client.post(url)
        
        # Garante que foi removida
        self.assertFalse(Fuelrequests.objects.filter(id=solicitacao.id).exists())

    def test_fluxo_anexar_comprovante(self):
        """Anexar comprovante com sucesso muda status para CONCLUÍDO."""
        solicitacao = Fuelrequests.objects.create(
            usuario=self.motorista,
            veiculo=self.veiculo,
            km_inicial=1000,
            km_final=1200,
            status=Fuelrequests.StatusChoices.APROVADO_AGUARDANDO
        )

        self.client.login(username='motorista_test', password='password123')
        url = reverse('reembolsos:anexar_comprovante', kwargs={'pk': solicitacao.id})
        
        data = {
            'comprovante_fiscal': self.fake_image
        }
        
        response = self.client.post(url, data)
        
        solicitacao.refresh_from_db()
        self.assertEqual(solicitacao.status, Fuelrequests.StatusChoices.CONCLUIDO)
        self.assertTrue(bool(solicitacao.comprovante_fiscal))