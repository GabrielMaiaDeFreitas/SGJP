"""
Testes do AtendimentoService que dependem de banco de dados.

Cobertura:
    - Cadastro válido (associações corretas)
    - Entidades / tabela de valores
    - Status operacional e financeiro
    - Atualização
    - Veículo rebocado
"""

from datetime import date, timedelta
from decimal import Decimal

import pytest

from app.services.atendimento_service import AtendimentoService

from app.exceptions.negocio import RegraNegocioError

from app.models import TabelaValores


# =============================================================
# 1. CADASTRO VÁLIDO
# =============================================================

class TestCadastroValido:

    def test_cria_atendimento_com_associacoes_corretas(
        self,
        db_session,
        formulario_valido,
        administradora,
        tipo_servico,
        tabela_valores,
        cliente,
        motorista,
        caminhao,
        usuario
    ):

        dados = AtendimentoService.montar_dados(
            formulario_valido
        )

        atendimento = AtendimentoService.salvar(

            dados=dados,

            id_usuario=usuario.id_usuario

        )

        assert atendimento.id_atendimento is not None

        assert (
            atendimento.fk_tabela_valores_id_tabela_valores
            == tabela_valores.id_tabela_valores
        )

        assert (
            atendimento.fk_cliente_id_cliente
            == cliente.id_cliente
        )

        assert (
            atendimento.fk_motorista_id_motorista
            == motorista.id_motorista
        )

        assert (
            atendimento.fk_caminhao_id_caminhao
            == caminhao.id_caminhao
        )

        assert (
            atendimento.fk_usuario_id_usuario
            == usuario.id_usuario
        )


# =============================================================
# 3. ENTIDADES / TABELA DE VALORES
# =============================================================

class TestEntidadesTabelaValores:

    def test_rejeita_quando_nao_existe_tabela_valores_ativa(
        self,
        db_session,
        administradora,
        tipo_servico,
        cliente,
        usuario
    ):
        # Note: propositalmente NÃO usa a fixture
        # `tabela_valores`, para simular a ausência
        # de uma tabela ativa para essa combinação.

        formulario = {

            "id_administradora": str(
                administradora.id_administradora
            ),

            "id_tipo_servico": str(
                tipo_servico.id_tipo_servico
            ),

            "id_cliente": str(
                cliente.id_cliente
            ),

        }

        dados = AtendimentoService.montar_dados(
            formulario
        )

        with pytest.raises(RegraNegocioError):

            AtendimentoService.salvar(

                dados=dados,

                id_usuario=usuario.id_usuario

            )


    def test_utiliza_apenas_tabela_valores_ativa(
        self,
        db_session,
        administradora,
        tipo_servico,
        cliente,
        usuario
    ):
        # Simula o cenário real: uma tabela antiga que foi
        # desativada (ativo=False) ao ser editada, e a nova
        # versão vigente (ativo=True) para a mesma
        # Administradora + Tipo de Serviço.

        tabela_antiga = TabelaValores(

            valor_saida=Decimal("80.00"),
            valor_km_excedente=Decimal("4.00"),
            ativo=False,

            fk_tipo_servico_id_tipo_servico=(
                tipo_servico.id_tipo_servico
            ),

            fk_administradora_id_administradora=(
                administradora.id_administradora
            )

        )

        tabela_ativa = TabelaValores(

            valor_saida=Decimal("120.00"),
            valor_km_excedente=Decimal("6.00"),
            ativo=True,

            fk_tipo_servico_id_tipo_servico=(
                tipo_servico.id_tipo_servico
            ),

            fk_administradora_id_administradora=(
                administradora.id_administradora
            )

        )

        db_session.add_all(
            [tabela_antiga, tabela_ativa]
        )

        db_session.commit()

        formulario = {

            "id_administradora": str(
                administradora.id_administradora
            ),

            "id_tipo_servico": str(
                tipo_servico.id_tipo_servico
            ),

            "id_cliente": str(
                cliente.id_cliente
            ),

        }

        dados = AtendimentoService.montar_dados(
            formulario
        )

        atendimento = AtendimentoService.salvar(

            dados=dados,

            id_usuario=usuario.id_usuario

        )

        assert (
            atendimento.fk_tabela_valores_id_tabela_valores
            == tabela_ativa.id_tabela_valores
        )

        assert (
            atendimento.fk_tabela_valores_id_tabela_valores
            != tabela_antiga.id_tabela_valores
        )


# =============================================================
# 8. VALOR TOTAL — COMPORTAMENTO ATUAL (SEM RECÁLCULO)
# =============================================================
#
# BRECHA DE REGRA DE NEGÓCIO / SEGURANÇA (pendência conhecida):
#
#   Hoje o cálculo de "valor_saida + km excedente + adicionais"
#   é feito inteiramente no JavaScript (atendimento.js), e o
#   AtendimentoService apenas armazena o `valor_total` que veio
#   no formulário, SEM validar se ele bate com o que a
#   TabelaValores + adicionais realmente resultariam.
#
#   Na prática, isso significa que uma requisição POST enviada
#   diretamente para a rota (sem passar pelo JS do navegador)
#   pode gravar qualquer `valor_total`, mesmo incompatível com
#   a tabela de valores vigente.
#
#   O teste abaixo documenta o comportamento ATUAL (valor
#   aceito como veio, sem recálculo) — ele não deve ser lido
#   como "correto do ponto de vista de negócio", apenas como
#   uma proteção contra regressão silenciosa nesse
#   comportamento existente. Recomenda-se, futuramente, mover
#   (ou duplicar, por segurança) o cálculo para o backend.
# =============================================================

class TestValorTotalComportamentoAtual:

    def test_valor_total_e_armazenado_exatamente_como_recebido(
        self,
        db_session,
        administradora,
        tipo_servico,
        cliente,
        usuario
    ):

        # Tabela de valores com valores bem diferentes do
        # valor_total que será enviado no formulário — para
        # deixar explícito que o backend não os cruza.

        tabela = TabelaValores(

            valor_saida=Decimal("999.00"),
            valor_km_excedente=Decimal("999.00"),
            ativo=True,

            fk_tipo_servico_id_tipo_servico=(
                tipo_servico.id_tipo_servico
            ),

            fk_administradora_id_administradora=(
                administradora.id_administradora
            )

        )

        db_session.add(tabela)
        db_session.commit()

        formulario = {

            "id_administradora": str(
                administradora.id_administradora
            ),

            "id_tipo_servico": str(
                tipo_servico.id_tipo_servico
            ),

            "id_cliente": str(
                cliente.id_cliente
            ),

            "km_total": "9999",

            "valor_total": "42.00",

        }

        dados = AtendimentoService.montar_dados(
            formulario
        )

        atendimento = AtendimentoService.salvar(

            dados=dados,

            id_usuario=usuario.id_usuario

        )

        # Comportamento atual: o valor é gravado exatamente
        # como veio do formulário, apesar de não ter nenhuma
        # relação matemática com valor_saida / valor_km_excedente
        # / km_total informados acima.

        assert atendimento.valor_total == Decimal("42.00")


# =============================================================
# 9. STATUS
# =============================================================

class TestStatus:

    def test_status_operacional_incompleto_quando_faltam_dados(
        self,
        administradora,
        tipo_servico
    ):
        # `definir_status` é um método que só opera sobre o
        # dicionário de dados — não precisa gravar nada no
        # banco, mas as fixtures de administradora/tipo_servico
        # garantem que o banco de teste já está criado
        # (via db_session, dependência indireta).

        dados = {

            "id_administradora": administradora.id_administradora,
            "id_tipo_servico": tipo_servico.id_tipo_servico,
            "id_cliente": None,
            "id_motorista": None,
            "id_caminhao": None,
            "data_atendimento": None,
            "protocolo": None,
            "placa_veiculo_rebocado": None,
            "modelo_veiculo_rebocado": None,
            "km_total": None,
            "valor_total": None,
            "valor_pago": Decimal("0.00"),
            "valor_pedagio": Decimal("0.00"),
            "pagamento_separado": False,

        }

        AtendimentoService.definir_status(
            dados
        )

        assert dados["status_operacional"] == "Incompleto"


    def test_status_operacional_completo_quando_todos_dados_presentes(
        self,
        administradora,
        tipo_servico,
        cliente,
        motorista,
        caminhao
    ):

        dados = {

            "id_administradora": administradora.id_administradora,
            "id_tipo_servico": tipo_servico.id_tipo_servico,
            "id_cliente": cliente.id_cliente,
            "id_motorista": motorista.id_motorista,
            "id_caminhao": caminhao.id_caminhao,
            "data_atendimento": date.today(),
            "protocolo": "PROT-0001",
            "placa_veiculo_rebocado": "ABC-1234",
            "modelo_veiculo_rebocado": "Modelo Teste",
            "km_total": Decimal("50"),
            "valor_total": Decimal("150.00"),
            "valor_pago": Decimal("0.00"),
            "valor_pedagio": Decimal("0.00"),
            "pagamento_separado": False,

        }

        AtendimentoService.definir_status(
            dados
        )

        assert dados["status_operacional"] == "Completo"


    def _dados_status_base(self, **overrides):

        base = {

            "id_administradora": 1,
            "id_tipo_servico": 1,
            "id_cliente": 1,
            "id_motorista": 1,
            "id_caminhao": 1,
            "data_atendimento": date.today(),
            "protocolo": "PROT-0001",
            "placa_veiculo_rebocado": "ABC-1234",
            "modelo_veiculo_rebocado": "Modelo Teste",
            "km_total": Decimal("50"),
            "valor_total": Decimal("150.00"),
            "valor_pago": Decimal("0.00"),
            "valor_pedagio": Decimal("0.00"),
            "pagamento_separado": False,

        }

        base.update(overrides)

        return base


    def test_status_financeiro_aguardando_fechamento_sem_pagamento(self):

        dados = self._dados_status_base()

        AtendimentoService.definir_status(
            dados
        )

        assert (
            dados["status_financeiro"]
            == "Aguardando Fechamento"
        )


    def test_status_financeiro_pagamento_parcial(self):

        dados = self._dados_status_base(
            valor_pago=Decimal("50.00")
        )

        AtendimentoService.definir_status(
            dados
        )

        assert (
            dados["status_financeiro"]
            == "Pagamento Parcial"
        )


    def test_status_financeiro_pago(self):

        dados = self._dados_status_base(
            valor_pago=Decimal("150.00")
        )

        AtendimentoService.definir_status(
            dados
        )

        assert dados["status_financeiro"] == "Pago"

# =============================================================
# 10. ATUALIZAÇÃO
# =============================================================

class TestAtualizacao:

    def test_atualiza_dados_e_mantem_tabela_valores_ativa(
        self,
        db_session,
        formulario_valido,
        administradora,
        tipo_servico,
        tabela_valores,
        cliente,
        motorista,
        caminhao,
        usuario
    ):

        dados_iniciais = AtendimentoService.montar_dados(
            formulario_valido
        )

        atendimento = AtendimentoService.salvar(

            dados=dados_iniciais,

            id_usuario=usuario.id_usuario

        )

        formulario_atualizado = dict(
            formulario_valido
        )

        formulario_atualizado["protocolo"] = "PROT-9999"
        formulario_atualizado["destino"] = "Novo Destino"
        formulario_atualizado["valor_total"] = "300.00"

        dados_atualizados = AtendimentoService.montar_dados(
            formulario_atualizado
        )

        atendimento_atualizado = AtendimentoService.atualizar(

            atendimento=atendimento,

            dados=dados_atualizados

        )

        assert atendimento_atualizado.protocolo == "PROT-9999"

        assert atendimento_atualizado.destino == "Novo Destino"

        assert (
            atendimento_atualizado.valor_total
            == Decimal("300.00")
        )

        assert (
            atendimento_atualizado.fk_tabela_valores_id_tabela_valores
            == tabela_valores.id_tabela_valores
        )


# =============================================================
# 11. VEÍCULO REBOCADO
# =============================================================

class TestVeiculoRebocado:

    def test_cria_veiculo_rebocado_quando_dados_informados(
        self,
        db_session,
        formulario_valido,
        usuario
    ):

        dados = AtendimentoService.montar_dados(
            formulario_valido
        )

        atendimento = AtendimentoService.salvar(

            dados=dados,

            id_usuario=usuario.id_usuario

        )

        assert atendimento.veiculo_rebocado is not None

        assert (
            atendimento.veiculo_rebocado.placa
            == "ABC-1234"
        )

        assert (
            atendimento.veiculo_rebocado.modelo
            == "Modelo Teste"
        )


    def test_nao_cria_veiculo_rebocado_quando_dados_ausentes(
        self,
        db_session,
        formulario_valido,
        usuario
    ):

        formulario = dict(
            formulario_valido
        )

        formulario["placa_veiculo_rebocado"] = ""
        formulario["modelo_veiculo_rebocado"] = ""

        dados = AtendimentoService.montar_dados(
            formulario
        )

        atendimento = AtendimentoService.salvar(

            dados=dados,

            id_usuario=usuario.id_usuario

        )

        assert atendimento.veiculo_rebocado is None