"""
Configuração global dos testes.

Estratégia de isolamento do banco de dados:
    - As variáveis de ambiente SECRET_KEY / DATABASE_URL são
      sobrescritas ANTES de qualquer import do pacote `app`,
      apontando para um arquivo SQLite temporário.
    - `python-dotenv` (usado em app/config.py) não sobrescreve
      variáveis já definidas no processo (override=False por
      padrão), então a definição feita aqui tem prioridade
      sobre um eventual .env com a URL do banco real.
    - Isso evita qualquer risco de os testes rodarem contra
      o banco de desenvolvimento/produção.

Cada teste roda com as tabelas recriadas do zero
(`create_all` / `drop_all`), garantindo isolamento total
entre um teste e outro (sem dependência de ordem de execução).
"""

import os
import sys
import tempfile

# Garante que a raiz do projeto (onde fica o pacote `app`)
# está no sys.path, independente de como/de onde o pytest
# for executado ou se o pytest.ini está sendo respeitado.
#
# __file__ = .../SGJP/tests/conftest.py
# _RAIZ_PROJETO = .../SGJP
_RAIZ_PROJETO = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if _RAIZ_PROJETO not in sys.path:

    sys.path.insert(
        0,
        _RAIZ_PROJETO
    )


_DB_FD, _DB_PATH = tempfile.mkstemp(
    suffix=".sqlite3",
    prefix="sgjp_test_"
)

os.environ["SECRET_KEY"] = "chave-de-teste"
os.environ["DATABASE_URL"] = f"sqlite:///{_DB_PATH}"


import pytest  # noqa: E402
from datetime import date, timedelta  # noqa: E402
from decimal import Decimal  # noqa: E402

from app import create_app, db as _db  # noqa: E402

from app.models import (  # noqa: E402
    Administradora,
    Cliente,
    Motorista,
    Caminhao,
    TipoServico,
    TabelaValores,
    Usuario
)


# =============================================================
# APP / BANCO DE DADOS
# =============================================================

@pytest.fixture(scope="session")
def app():

    application = create_app()

    application.config["TESTING"] = True

    yield application

    with application.app_context():

        _db.engine.dispose()

    os.close(_DB_FD)

    os.remove(_DB_PATH)


@pytest.fixture
def db_session(app):
    """
    Fixture principal usada por todos os testes que precisam
    de banco de dados. Recria as tabelas antes de cada teste
    e as remove ao final, garantindo isolamento total.
    """

    with app.app_context():

        _db.create_all()

        yield _db.session

        _db.session.remove()

        _db.drop_all()


# =============================================================
# ENTIDADES BASE
# =============================================================

@pytest.fixture
def administradora(db_session):

    obj = Administradora(

        nome="Administradora Teste",
        cliente_proprio=False,
        ativo=True

    )

    db_session.add(obj)
    db_session.commit()

    return obj


@pytest.fixture
def tipo_servico(db_session):

    obj = TipoServico(

        nome="Reboque",
        ativo=True

    )

    db_session.add(obj)
    db_session.commit()

    return obj


@pytest.fixture
def tabela_valores(db_session, administradora, tipo_servico):

    obj = TabelaValores(

        valor_saida=Decimal("100.00"),
        valor_km_excedente=Decimal("5.00"),
        ativo=True,

        fk_tipo_servico_id_tipo_servico=(
            tipo_servico.id_tipo_servico
        ),

        fk_administradora_id_administradora=(
            administradora.id_administradora
        )

    )

    db_session.add(obj)
    db_session.commit()

    return obj


@pytest.fixture
def cliente(db_session, administradora):

    obj = Cliente(

        nome_fantasia="Cliente Teste",
        cnpj="00.000.000/0001-00",
        razao_social="Cliente Teste LTDA",
        ativo=True,

        fk_administradora_id_administradora=(
            administradora.id_administradora
        )

    )

    db_session.add(obj)
    db_session.commit()

    return obj


@pytest.fixture
def motorista(db_session):

    obj = Motorista(

        matricula="M-0001",
        nome="Motorista Teste",
        numero_cnh="12345678900",
        validade_cnh=date.today() + timedelta(days=365),
        validade_toxicologico=date.today() + timedelta(days=180),
        categoria_cnh="E",
        ativo=True

    )

    db_session.add(obj)
    db_session.commit()

    return obj


@pytest.fixture
def caminhao(db_session):

    obj = Caminhao(

        placa="ABC1D23",
        modelo="Caminhão Teste",
        ativo=True

    )

    db_session.add(obj)
    db_session.commit()

    return obj


@pytest.fixture
def usuario(db_session):

    obj = Usuario(

        nome="Usuário Teste",
        login="usuario.teste",
        perfil="Operador",
        ativo=True

    )

    obj.set_senha("senha-teste-123")

    db_session.add(obj)
    db_session.commit()

    return obj


# =============================================================
# FORMULÁRIO PADRÃO (dados válidos completos)
# =============================================================

@pytest.fixture
def formulario_valido(
    administradora,
    tipo_servico,
    tabela_valores,
    cliente,
    motorista,
    caminhao
):
    """
    Monta um dicionário equivalente a um `request.form` válido
    e completo, pronto para ser passado a
    AtendimentoService.montar_dados().

    Testes individuais podem copiar este dicionário e
    sobrescrever/remover chaves específicas conforme o cenário.
    """

    return {

        "id_administradora": str(
            administradora.id_administradora
        ),

        "id_tipo_servico": str(
            tipo_servico.id_tipo_servico
        ),

        "id_cliente": str(
            cliente.id_cliente
        ),

        "id_motorista": str(
            motorista.id_motorista
        ),

        "id_caminhao": str(
            caminhao.id_caminhao
        ),

        "data_atendimento": date.today().isoformat(),

        "protocolo": "PROT-0001",

        "origem": "Origem Teste",

        "destino": "Destino Teste",

        "km_total": "50",

        "valor_total": "150.00",

        "placa_veiculo_rebocado": "ABC-1234",

        "modelo_veiculo_rebocado": "Modelo Teste",

    }