# FuelProject

Sistema de gestão de frotas e reembolsos, desenvolvido em Django, com foco em controle de veículos, solicitações de combustível e reembolsos de despesas.

## 📋 Sobre o projeto

O FuelProject centraliza o controle de uma frota de veículos, permitindo o registro de usuários, veículos, solicitações de abastecimento (fuel requests) e reembolsos, com uma arquitetura organizada em apps Django independentes.

## 🚀 Funcionalidades

- **Usuários**: cadastro e gerenciamento de usuários do sistema
- **Veículos**: controle da frota (cadastro, dados e vínculo com usuários)
- **Solicitações de combustível**: fluxo de pedidos de abastecimento
- **Reembolsos**: registro e acompanhamento de reembolsos de despesas
- **Utils**: funções e utilidades compartilhadas entre os apps

## 🛠️ Tecnologias

- **Python** / **Django 6.0.3**
- **PostgreSQL** (via `psycopg2`)
- **Docker** e **Docker Compose**
- **Nginx** + **Gunicorn** (deploy em produção)
- **Pytest** (TDD)
- **python-dotenv** (variáveis de ambiente)

## 📁 Estrutura do projeto

```
fuelproject/
├── FuelProject/       # Configurações principais do projeto Django
├── fuelrequests/      # App de solicitações de combustível
├── reembolsos/        # App de reembolsos
├── usuarios/          # App de usuários
├── veiculos/          # App de veículos
├── utils/             # Funções utilitárias compartilhadas
├── static/            # Arquivos estáticos
├── templates/         # Templates HTML
├── tests/             # Testes automatizados
├── DOCKERFILE
├── dcoker-compose.yml
├── manage.py
├── pytest.ini
├── requirements.txt
└── .env.example
```

## ⚙️ Como rodar localmente

### Pré-requisitos
- Python 3.x
- PostgreSQL
- Docker e Docker Compose (opcional, para subir via container)

### Via ambiente virtual

```bash
# Clone o repositório
git clone https://github.com/machadopy/fuelproject.git
cd fuelproject

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com suas credenciais de banco de dados

# Rode as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```

### Via Docker

```bash
docker compose -f dcoker-compose.yml up --build
```

## ✅ Testes

O projeto segue TDD, com testes escritos em Pytest:

```bash
pytest
```

## 📄 Licença

Este projeto possui direitos autorais reservados. Consulte o arquivo `LICENSE.TXT` para mais detalhes sobre os termos de uso — o código é disponibilizado apenas para fins de visualização de portfólio.

## 📬 Contato

Marcio Vitor Machado
