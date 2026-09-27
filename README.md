# SGJP — Sistema de Gerenciamento da JP Transportes

Sistema web desenvolvido para gerenciamento operacional da **JP Transportes**, com foco no controle de atendimentos, clientes, motoristas, caminhões, administradoras e tabelas de valores.

O projeto foi desenvolvido utilizando **Python**, **Flask** e **SQLAlchemy**, seguindo uma arquitetura **MVC em camadas** com separação entre Models, Routes, Services e Views.

---

# Autor

* **Gabriel Maia de Freitas**

---

# Tecnologias Utilizadas

* Python 3
* Flask
* SQLAlchemy
* Flask-Migrate (Alembic)
* SQLite
* Jinja2
* HTML5
* CSS3
* JavaScript
* MVC em Camadas (Model • View • Controller + Service)

---

# Principais Funcionalidades

## Autenticação

* Login de usuários
* Controle de sessão
* Perfis de acesso
* Logout

## Cadastros

* Usuários
* Caminhões
* Motoristas
* Administradoras
* Clientes
* Tipos de Serviço
* Tabelas de Valores

## Recursos Gerais

* Filtros dinâmicos
* Visualização completa dos módulos
* Exportação para Excel e PDF
* Ativação e desativação de registros
* Versionamento de Tabelas de Valores

---

# Arquitetura do Projeto

O projeto segue uma arquitetura **MVC em camadas**, onde cada responsabilidade é isolada em um diretório específico.

```text
app/
│
├── models/          # Entidades do banco
├── routes/          # Controllers (Blueprints)
├── services/        # Regras de negócio
├── filters/         # Configuração dos filtros
├── exports/         # Excel / PDF / CSV
├── templates/       # Views (Jinja2)
├── static/
│   ├── css/
│   └── js/
│
├── constants/
└── utils/

migrations/
tests/
run.py
README.md
```

---

# Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/SGJP.git
cd SGJP
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

# Banco de Dados

Crie todas as tabelas utilizando as migrations:

```bash
flask db upgrade
```

Caso seja a primeira execução do projeto:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

# Executando a Aplicação

Inicie o servidor Flask:

```bash
python run.py
```

A aplicação ficará disponível em:

```text
http://localhost:5000
```

---

# Estrutura dos Módulos

| Módulo             | Descrição                                                    |
| ------------------ | ------------------------------------------------------------ |
| Usuários           | Controle de acesso e autenticação                            |
| Caminhões          | Cadastro e gerenciamento da frota                            |
| Motoristas         | Controle de documentos e validade                            |
| Administradoras    | Empresas responsáveis pelos atendimentos                     |
| Clientes           | Clientes vinculados às administradoras                       |
| Tipos de Serviço   | Serviços prestados pela empresa                              |
| Tabelas de Valores | Valores por administradora e tipo de serviço                 |
| Atendimento        | Controle operacional dos atendimentos *(em desenvolvimento)* |

---

# Capturas de Tela

## Login

**(Inserir imagem: `images/login.png`)**

---

## Dashboard

**(Inserir imagem: `images/dashboard.png`)**

---

## Gerenciamento de Usuários

**(Inserir imagem: `images/usuarios.png`)**

---

## Gerenciamento de Caminhões

**(Inserir imagem: `images/caminhoes.png`)**

---

## Gerenciamento de Motoristas

**(Inserir imagem: `images/motoristas.png`)**

---

## Gerenciamento de Administradoras

**(Inserir imagem: `images/administradoras.png`)**

---

## Gerenciamento de Clientes

**(Inserir imagem: `images/clientes.png`)**

---

## Gerenciamento de Tipos de Serviço

**(Inserir imagem: `images/tipos_servico.png`)**

---

## Gerenciamento de Tabelas de Valores

**(Inserir imagem: `images/tabelas_valores.png`)**

---

## Exportação de Dados

**(Inserir imagem: `images/exportacao.png`)**

---

# Diferenciais do Projeto

* Arquitetura MVC em camadas com separação de responsabilidades.
* Camada de **Services** para centralizar toda a regra de negócio.
* Sistema de filtros reutilizável entre todos os módulos.
* Exportação padronizada para Excel e PDF.
* Versionamento das Tabelas de Valores preservando histórico.
* Relacionamentos utilizando **SQLAlchemy** com `back_populates`.

---

# Status do Projeto

**Em desenvolvimento**

Próximo módulo em implementação:

* Atendimento
* Integração com Google Routes API
* Dashboard operacional
* Controle de fechamento e pagamentos

---

# Licença

Projeto desenvolvido para fins acadêmicos e de aprendizado no **Instituto Federal de Goiás (IFG) – Campus Anápolis**.
