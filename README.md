# SGJP — Sistema de Gestão da JP Transportes

Sistema web desenvolvido em Flask para gerenciamento das operações da JP Transportes.

---

## 📋 Sobre o projeto

O SGJP (Sistema de Gestão da JP Transportes) é uma aplicação web desenvolvida em Python utilizando o framework Flask.

A aplicação possui módulos para gerenciamento de:

- Usuários
- Motoristas
- Caminhões
- Clientes
- Administradoras
- Tipos de serviço
- Tabelas de valores
- Atendimentos
- Exportações
- Relatórios

A aplicação utiliza banco de dados SQLite e SQLAlchemy para persistência dos dados.

---

## 🛠️ Tecnologias utilizadas

- Python 3.13
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy
- SQLite
- Flask-WTF
- WTForms
- python-dotenv
- ReportLab
- OpenPyXL
- Requests
- Pytest

As versões das dependências utilizadas no projeto estão registradas no arquivo:

```text
requirements.txt
```

---

## 📦 Requisitos

Para executar o projeto, é necessário ter instalado:

- Python 3.13.x
- Git

O projeto foi desenvolvido e testado em Windows.

---

## 🚀 Instalação

### 1. Clonar o repositório

```powershell
git clone https://github.com/GabrielMaiaDeFreitas/SGJP.git
```

Entrar na pasta do projeto:

```powershell
cd SGJP
```

### 2. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 3. Ativar o ambiente virtual

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Após a ativação, o terminal deverá apresentar:

```text
(.venv)
```

Caso o PowerShell bloqueie a execução do script, execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois tente novamente:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

Com a `.venv` ativada:

```powershell
pip install -r requirements.txt
```

---

## 🔐 Configuração do ambiente

O projeto utiliza variáveis de ambiente através do arquivo `.env`.

Crie um arquivo `.env` na raiz do projeto:

```powershell
notepad .env
```

Adicione:

```env
SECRET_KEY=sua_chave_secreta
DATABASE_URL=sqlite:///sgjp.db
GOOGLE_MAPS_API_KEY=sua_chave_google_maps
ADMIN_PASSWORD=sua_senha_administrador
```

### Variáveis utilizadas

#### SECRET_KEY

Chave utilizada pelo Flask para recursos que dependem de segurança da aplicação.

```env
SECRET_KEY=sua_chave_secreta
```

#### DATABASE_URL

Define a conexão utilizada pelo SQLAlchemy.

Na configuração atual:

```env
DATABASE_URL=sqlite:///sgjp.db
```

#### GOOGLE_MAPS_API_KEY

Chave utilizada para integração com a API do Google Maps.

```env
GOOGLE_MAPS_API_KEY=sua_chave_google_maps
```

#### ADMIN_PASSWORD

Senha utilizada pelo `seed.py` para criação do usuário administrador inicial.

```env
ADMIN_PASSWORD=sua_senha_administrador
```

> ⚠️ Nunca publique os valores reais dessas variáveis no GitHub.

---

## 🗄️ Banco de dados

O projeto utiliza SQLite.

A estrutura do banco de dados é controlada através do Flask-Migrate/Alembic.

O banco não deve ser criado manualmente.

### Criar ou atualizar o banco

Com a `.venv` ativada e o `.env` configurado:

```powershell
flask --app run db upgrade
```

Esse comando aplica as migrations existentes e cria ou atualiza a estrutura do banco de dados.

---

## 👤 Criar usuário administrador

Após executar as migrations:

```powershell
python seed.py
```

O script verifica se já existe um usuário com o login:

```text
admin
```

Caso não exista, será criado um usuário administrador utilizando a senha definida em:

```env
ADMIN_PASSWORD=sua_senha_administrador
```

Caso o usuário `admin` já exista, nenhum novo usuário será criado.

---

## ▶️ Executar o sistema

Com a `.venv` ativada:

```powershell
python run.py
```

A aplicação poderá ser acessada pelo navegador através de:

```text
http://127.0.0.1:5000
```

---

## 🌐 Execução em servidor

Para disponibilizar a aplicação para conexões externas, o `run.py` pode ser configurado para escutar todas as interfaces de rede:

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
```

Nesse caso, a aplicação poderá receber conexões através da rede da máquina onde está sendo executada.

> A configuração de rede, firewall, domínio, HTTPS e servidor de produção deve ser definida de acordo com o ambiente de hospedagem.

---

## 🧪 Testes

Os testes automatizados estão localizados no diretório:

```text
tests/
```

Para executar todos os testes:

```powershell
pytest
```

Para executar um arquivo de teste específico:

```powershell
pytest caminho/do/teste.py
```

---

## 🔄 Atualizar o sistema

Para obter as alterações mais recentes do repositório:

```powershell
git pull
```

Caso as dependências tenham sido alteradas:

```powershell
pip install -r requirements.txt
```

Caso existam novas migrations:

```powershell
flask --app run db upgrade
```

---

## 📌 Instalação rápida

Para uma instalação do zero:

```powershell
git clone https://github.com/GabrielMaiaDeFreitas/SGJP.git

cd SGJP

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Depois configure o arquivo `.env`:

```powershell
notepad .env
```

Configure:

```env
SECRET_KEY=sua_chave_secreta
DATABASE_URL=sqlite:///sgjp.db
GOOGLE_MAPS_API_KEY=sua_chave_google_maps
ADMIN_PASSWORD=sua_senha_administrador
```

Depois execute:

```powershell
flask --app run db upgrade

python seed.py

python run.py
```

Acesse:

```text
http://127.0.0.1:5000
```

---

## 📁 Estrutura do projeto

```text
SGJP/
│
├── app/
│   ├── constants/
│   ├── exceptions/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── config.py
│   └── __init__.py
│
├── migrations/
│   ├── versions/
│   └── ...
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
├── seed.py
└── README.md
```

---

## ⚠️ Arquivos que não devem ser versionados

Os seguintes arquivos e diretórios não devem ser enviados ao GitHub:

```text
.env
.venv/
*.db
*.sqlite
*.sqlite3
__pycache__/
.pytest_cache/
```

Esses arquivos estão protegidos pelo `.gitignore`.

---

## 🔒 Segurança

Nunca publique no repositório:

- `SECRET_KEY`
- `ADMIN_PASSWORD`
- `GOOGLE_MAPS_API_KEY`
- Senhas de usuários
- Credenciais de banco de dados
- Outras informações sensíveis

As credenciais devem ser configuradas diretamente no ambiente onde a aplicação será executada.

---

## 🔄 Fluxo completo de instalação

```text
1. Clonar o repositório
        ↓
2. Entrar na pasta SGJP
        ↓
3. Criar o ambiente virtual
        ↓
4. Ativar o ambiente virtual
        ↓
5. Instalar requirements.txt
        ↓
6. Criar e configurar o .env
        ↓
7. Executar as migrations
        ↓
8. Executar o seed.py
        ↓
9. Executar o run.py
        ↓
10. Acessar pelo navegador
```

---

## 👨‍💻 Desenvolvimento

Durante o desenvolvimento, recomenda-se trabalhar utilizando um ambiente virtual (`.venv`) separado.

Quando novas dependências forem adicionadas ao projeto, o arquivo `requirements.txt` deve ser atualizado.

Para gerar o arquivo novamente:

```powershell
pip freeze > requirements.txt
```

---

## 📄 Observações

O SGJP foi desenvolvido como parte das atividades acadêmicas do curso de Ciência da Computação do Instituto Federal de Goiás (IFG).

O ambiente de produção deve possuir configurações próprias de segurança, banco de dados, servidor web e gerenciamento de processos, conforme a infraestrutura escolhida para hospedagem.