"""
Testes das validações "puras" do AtendimentoService.

Estes testes NÃO tocam banco de dados: testam apenas
métodos estáticos que recebem um dicionário de dados
e retornam ou levantam exceção.

Cobertura:
    - Campos obrigatórios (montar_dados)
    - Data (validar_data)
    - Valores negativos (validar_valores)
    - Quantidades negativas (validar_quantidades)
    - Placa do veículo rebocado (validar_veiculo_rebocado)
    - Regras condicionais de cobrança (validar_campos_condicionais)
"""

from datetime import date, timedelta
from decimal import Decimal

import pytest

from app.services.atendimento_service import AtendimentoService

from app.exceptions.validacao import (
    CampoObrigatorioError,
    DataInvalidaError,
    PlacaInvalidaError,
    ValorInvalidoError
)


# =============================================================
# HELPERS
# =============================================================

def _dados_condicionais_base(**overrides):
    """
    Monta um dicionário mínimo válido para os métodos
    que operam sobre "dados" já processados por
    montar_dados(), permitindo sobrescrever campos
    específicos em cada teste.
    """

    base = {

        "data_atendimento": None,

        "km_total": None,
        "valor_total": None,
        "valor_pago": Decimal("0.00"),
        "valor_pedagio": Decimal("0.00"),

        "quantidade_hora_parada": 0,
        "quantidade_hora_trabalhada": 0,
        "quantidade_patins": 0,

        "houve_pedagio": False,
        "cobrar_pedagio": False,
        "cobrar_hora_parada": False,
        "cobrar_hora_trabalhada": False,
        "usar_patins": False,

        "placa_veiculo_rebocado": None,
        "modelo_veiculo_rebocado": None,

    }

    base.update(overrides)

    return base


# =============================================================
# CAMPOS OBRIGATÓRIOS (montar_dados)
# =============================================================

class TestCamposObrigatorios:

    def test_rejeita_sem_administradora(self):

        formulario = {

            "id_administradora": "",
            "id_tipo_servico": "1"

        }

        with pytest.raises(CampoObrigatorioError) as excinfo:

            AtendimentoService.montar_dados(
                formulario
            )

        assert excinfo.value.campo == "Administradora"


    def test_rejeita_sem_tipo_servico(self):

        formulario = {

            "id_administradora": "1",
            "id_tipo_servico": ""

        }

        with pytest.raises(CampoObrigatorioError) as excinfo:

            AtendimentoService.montar_dados(
                formulario
            )

        assert excinfo.value.campo == "Tipo de Serviço"


# =============================================================
# DATA
# =============================================================

class TestData:

    def test_aceita_data_valida(self):

        dados = _dados_condicionais_base(
            data_atendimento=date.today()
        )

        # Não deve levantar nenhuma exceção.

        AtendimentoService._validar_data(
            dados
        )


    def test_aceita_data_passada(self):

        dados = _dados_condicionais_base(
            data_atendimento=date.today() - timedelta(days=5)
        )

        AtendimentoService._validar_data(
            dados
        )


    def test_rejeita_data_futura(self):

        dados = _dados_condicionais_base(
            data_atendimento=date.today() + timedelta(days=1)
        )

        with pytest.raises(DataInvalidaError):

            AtendimentoService._validar_data(
                dados
            )


    def test_aceita_atendimento_sem_data(self):

        dados = _dados_condicionais_base(
            data_atendimento=None
        )

        # Atendimento pode ser criado sem data.

        AtendimentoService._validar_data(
            dados
        )


# =============================================================
# VALORES NEGATIVOS
# =============================================================

class TestValoresNegativos:

    def test_rejeita_km_total_negativo(self):

        dados = _dados_condicionais_base(
            km_total=Decimal("-1")
        )

        with pytest.raises(ValorInvalidoError) as excinfo:

            AtendimentoService._validar_valores(
                dados
            )

        assert excinfo.value.campo == "km_total"


    def test_rejeita_valor_pedagio_negativo(self):

        dados = _dados_condicionais_base(
            valor_pedagio=Decimal("-10.00")
        )

        with pytest.raises(ValorInvalidoError) as excinfo:

            AtendimentoService._validar_valores(
                dados
            )

        assert excinfo.value.campo == "valor_pedagio"


    def test_rejeita_quantidade_hora_parada_negativa(self):

        dados = _dados_condicionais_base(
            quantidade_hora_parada=-1
        )

        with pytest.raises(ValorInvalidoError) as excinfo:

            AtendimentoService._validar_quantidades(
                dados
            )

        assert excinfo.value.campo == "quantidade_hora_parada"


    def test_rejeita_quantidade_hora_trabalhada_negativa(self):

        dados = _dados_condicionais_base(
            quantidade_hora_trabalhada=-1
        )

        with pytest.raises(ValorInvalidoError) as excinfo:

            AtendimentoService._validar_quantidades(
                dados
            )

        assert excinfo.value.campo == "quantidade_hora_trabalhada"


    def test_rejeita_quantidade_patins_negativa(self):

        dados = _dados_condicionais_base(
            quantidade_patins=-1
        )

        with pytest.raises(ValorInvalidoError) as excinfo:

            AtendimentoService._validar_quantidades(
                dados
            )

        assert excinfo.value.campo == "quantidade_patins"


# =============================================================
# PLACA DO VEÍCULO REBOCADO
# =============================================================

class TestPlacaVeiculoRebocado:

    @pytest.mark.parametrize(
        "placa",
        [
            "ABC-1234",
            "ABC1D23",
        ]
    )
    def test_aceita_placa_valida(self, placa):

        dados = _dados_condicionais_base(
            placa_veiculo_rebocado=placa
        )

        # Não deve levantar nenhuma exceção.

        AtendimentoService._validar_veiculo_rebocado(
            dados
        )


    def test_rejeita_placa_invalida(self):

        dados = _dados_condicionais_base(
            placa_veiculo_rebocado="XXXX-99"
        )

        with pytest.raises(PlacaInvalidaError):

            AtendimentoService._validar_veiculo_rebocado(
                dados
            )


    def test_nao_exige_placa_nem_modelo(self):

        dados = _dados_condicionais_base(
            placa_veiculo_rebocado=None,
            modelo_veiculo_rebocado=None
        )

        # Veículo rebocado é totalmente opcional.

        AtendimentoService._validar_veiculo_rebocado(
            dados
        )


# =============================================================
# REGRAS CONDICIONAIS DE COBRANÇA
# =============================================================

class TestCamposCondicionais:

    def test_hora_parada_ativa_exige_quantidade_maior_que_zero(self):

        dados = _dados_condicionais_base(
            cobrar_hora_parada=True,
            quantidade_hora_parada=0
        )

        with pytest.raises(ValorInvalidoError) as excinfo:

            AtendimentoService._validar_campos_condicionais(
                dados
            )

        assert excinfo.value.campo == "quantidade_hora_parada"


    def test_hora_parada_inativa_nao_exige_quantidade(self):

        dados = _dados_condicionais_base(
            cobrar_hora_parada=False,
            quantidade_hora_parada=0
        )

        AtendimentoService._validar_campos_condicionais(
            dados
        )


    def test_hora_trabalhada_ativa_exige_quantidade_maior_que_zero(self):

        dados = _dados_condicionais_base(
            cobrar_hora_trabalhada=True,
            quantidade_hora_trabalhada=0
        )

        with pytest.raises(ValorInvalidoError) as excinfo:

            AtendimentoService._validar_campos_condicionais(
                dados
            )

        assert excinfo.value.campo == "quantidade_hora_trabalhada"


    def test_patins_ativo_exige_quantidade_maior_que_zero(self):

        dados = _dados_condicionais_base(
            usar_patins=True,
            quantidade_patins=0
        )

        with pytest.raises(ValorInvalidoError) as excinfo:

            AtendimentoService._validar_campos_condicionais(
                dados
            )

        assert excinfo.value.campo == "quantidade_patins"


    def test_houve_pedagio_exige_valor_maior_que_zero(self):

        dados = _dados_condicionais_base(
            houve_pedagio=True,
            valor_pedagio=Decimal("0.00")
        )

        with pytest.raises(ValorInvalidoError) as excinfo:

            AtendimentoService._validar_campos_condicionais(
                dados
            )

        assert excinfo.value.campo == "valor_pedagio"


    def test_houve_pedagio_falso_nao_exige_valor(self):

        dados = _dados_condicionais_base(
            houve_pedagio=False,
            valor_pedagio=Decimal("0.00")
        )

        AtendimentoService._validar_campos_condicionais(
            dados
        )