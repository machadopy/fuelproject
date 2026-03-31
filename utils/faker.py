import random
from faker import Faker
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from veiculos.models import Veiculo
from fuelrequests.models import Fuelrequests

fake = Faker('pt_BR')  # Configurado para português do Brasil
User = get_user_model()

# Marcas e modelos de carros brasileiros
MARCAS_MODELOS = [
    ('Fiat', 'Uno'),
    ('Fiat', 'Palio'),
    ('VW', 'Gol'),
    ('VW', 'Fox'),
    ('Chevrolet', 'Celta'),
    ('Chevrolet', 'Onix'),
    ('Renault', 'Logan'),
    ('Hyundai', 'HB20'),
    ('Ford', 'Fiesta'),
    ('Peugeot', '207'),
]

def gerar_data_aleatoria():
    """Gera uma data aleatória entre agora e 2 anos no passado"""
    dias_atras = random.randint(0, 730)  # 730 dias = ~2 anos
    data = timezone.now() - timedelta(days=dias_atras)
    return data.date()

def gerar_usuarios_com_faker(n=5):
    """Gera novos usuários aleatórios"""
    usuarios_criados = []
    for _ in range(n):
        nome = fake.name()
        username = fake.user_name()[:15]  # Limita a 15 caracteres
        
        # Evita duplicatas de username
        while User.objects.filter(username=username).exists():
            username = fake.user_name()[:15]
        
        usuario = User.objects.create_user(
            username=username,
            email=fake.email(),
            first_name=nome.split()[0],
            last_name=' '.join(nome.split()[1:]) if len(nome.split()) > 1 else ''
        )
        usuarios_criados.append(usuario)
        print(f"✅ Usuário Criado: {usuario.username} ({usuario.first_name})")
    
    return usuarios_criados

def gerar_veiculos_com_faker(n=5):
    """Gera novos veículos aleatórios"""
    veiculos_criados = []
    for _ in range(n):
        marca, modelo = random.choice(MARCAS_MODELOS)
        placa = fake.license_plate()[:7].upper()
        
        # Evita duplicatas de placa
        while Veiculo.objects.filter(placa=placa).exists():
            placa = fake.license_plate()[:7].upper()
        
        veiculo = Veiculo.objects.create(
            placa=placa,
            marca=marca,
            modelo=modelo,
            km=fake.random.randint(5000, 150000)
        )
        veiculos_criados.append(veiculo)
        print(f"✅ Veículo Criado: {veiculo.marca} {veiculo.modelo} ({veiculo.placa})")
    
    return veiculos_criados

def gerar_solicitacoes_com_faker(n=15):
    """Gera novas solicitações de combustível"""
    usuarios = User.objects.all()
    veiculos = Veiculo.objects.all()

    if not usuarios.exists() or not veiculos.exists():
        print("Erro: Cadastre ao menos um Usuário e um Veículo antes de rodar.")
        return

    for _ in range(n):
        # Gerando dados aleatórios
        km_ini = fake.random.randint(1000, 90000)
        km_fin = km_ini + fake.random.randint(10, 1000)
        
        solicitacao = Fuelrequests.objects.create(
            usuario=random.choice(usuarios),
            veiculo=random.choice(veiculos),
            km_inicial=km_ini,
            km_final=km_fin,
            status=random.choice(['P', 'A', 'N'])
        )
        
        # Atualizando a data para uma aleatória (entre agora e 2 anos atrás)
        solicitacao.data_solicitacao = gerar_data_aleatoria()
        solicitacao.save(update_fields=['data_solicitacao'])
        
        print(f"✅ Solicitação Gerada: ID {solicitacao.id} | Usuário: {solicitacao.usuario.username} | Veículo: {solicitacao.veiculo} | Data: {solicitacao.data_solicitacao}")

    print(f"\n✅ {n} solicitações fakes inseridas com sucesso!")

def gerar_dados_completos(usuarios=5, veiculos=5, solicitacoes=15):
    """Gera usuários, veículos e solicitações de uma vez"""
    print("\n" + "="*60)
    print("🚀 GERANDO DADOS FAKE COMPLETOS")
    print("="*60 + "\n")
    
    print(f"📝 Gerando {usuarios} usuários...")
    gerar_usuarios_com_faker(usuarios)
    
    print(f"\n🚗 Gerando {veiculos} veículos...")
    gerar_veiculos_com_faker(veiculos)
    
    print(f"\n⛽ Gerando {solicitacoes} solicitações...")
    gerar_solicitacoes_com_faker(solicitacoes)
    
    print("\n" + "="*60)
    print("✨ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("="*60)