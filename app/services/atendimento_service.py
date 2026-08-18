from datetime import date
from decimal import Decimal, InvalidOperation

from app import db

from app.models import (
    Atendimento,
    Administradora,
    Motorista,
    Caminhao,
    Cliente,
    TipoServico,
    TabelaValores,
    VeiculoRebocado
)

from app.filters.atendimento import FILTROS_ATENDIMENTO

from app.services.filter_service import FilterService
from app.services.tabela_valores_service import TabelaValoresService
from app.services.google_maps_service import GoogleMapsService

from app.constants.atendimento import (
    VALOR_PATINS,
    VALOR_HORA_PARADA,
    VALOR_HORA_TRABALHADA,
    KM_FRANQUIA,
    STATUS_OPERACIONAL_PADRAO,
    STATUS_OPERACIONAL_PENDENTE,
    STATUS_OPERACIONAL_COMPLETO,
    STATUS_FINANCEIRO_AGUARDANDO_FECHAMENTO,
    STATUS_FINANCEIRO_AGUARDANDO_PAGAMENTO,
    STATUS_FINANCEIRO_PAGAMENTO_PARCIAL,
    STATUS_FINANCEIRO_PAGO
)

from app.exceptions.negocio import (
    RegraNegocioError,
    RecursoNaoEncontradoError,
    RecursoDuplicadoError,
    RecursoEmUsoError
)

from app.exceptions.validacao import (
    ValidacaoError,
    CampoObrigatorioError,
    FormatoInvalidoError,
    PlacaInvalidaError,
    DataInvalidaError,
    ValorInvalidoError
)

from sqlalchemy.orm import joinedload

class AtendimentoService:

    # =========================================================
    # CONVERSÕES
    # =========================================================

    @staticmethod
    def _inteiro(
        valor,
        campo
    ):

        if valor is None or str(valor).strip() == "":

            raise CampoObrigatorioError(
                campo
            )

        try:

            return int(valor)

        except (TypeError, ValueError):

            raise FormatoInvalidoError(
                campo
            )


    @staticmethod
    def _inteiro_ou_none(
        valor,
        campo
    ):

        if valor is None or str(valor).strip() == "":

            return None

        try:

            return int(valor)

        except (TypeError, ValueError):

            raise FormatoInvalidoError(
                campo
            )

    @staticmethod
    def _inteiro_ou_zero(valor):

        if valor is None or str(valor).strip() == "":
            return 0

        try:

            return int(valor)

        except (TypeError, ValueError):

            raise FormatoInvalidoError(
                "Quantidade"
            )


    @staticmethod
    def _decimal(valor):

        if valor is None or str(valor).strip() == "":

            return Decimal("0.00")

        try:

            return Decimal(
                str(valor)
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            raise FormatoInvalidoError(
                "valor"
            )


    @staticmethod
    def _decimal_ou_none(valor):

        if valor is None or str(valor).strip() == "":

            return None

        try:

            return Decimal(
                str(valor)
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            raise FormatoInvalidoError(
                "valor"
            )


    # =========================================================
    # MONTAGEM DOS DADOS DO FORMULÁRIO
    # =========================================================

    @staticmethod
    def montar_dados(formulario):

        # ============================================================
        # CAMPOS OBRIGATÓRIOS
        # ============================================================

        id_administradora = formulario.get(
            "id_administradora"
        )

        if not id_administradora:

            raise CampoObrigatorioError(
                "Administradora"
            )


        id_tipo_servico = formulario.get(
            "id_tipo_servico"
        )

        if not id_tipo_servico:

            raise CampoObrigatorioError(
                "Tipo de Serviço"
            )


        # ============================================================
        # DATA DO ATENDIMENTO
        # ============================================================

        data_atendimento = None

        valor_data = formulario.get(
            "data_atendimento"
        )

        if valor_data:

            try:

                data_atendimento = date.fromisoformat(
                    valor_data
                )

            except ValueError:

                raise DataInvalidaError(
                    "A data do atendimento possui formato inválido."
                )


        # ============================================================
        # VEÍCULO REBOCADO
        # ============================================================

        placa_veiculo_rebocado = (
            formulario.get(
                "placa_veiculo_rebocado"
            )
            or ""
        ).strip()

        modelo_veiculo_rebocado = (
            formulario.get(
                "modelo_veiculo_rebocado"
            )
            or ""
        ).strip()


        # ============================================================
        # DADOS DO ATENDIMENTO
        # ============================================================

        return {

            "id_administradora":
                AtendimentoService._inteiro(
                    id_administradora,
                    "Administradora"
                ),

            "id_tipo_servico":
                AtendimentoService._inteiro(
                    id_tipo_servico,
                    "Tipo de Serviço"
                ),

            "id_cliente":
                AtendimentoService._inteiro_ou_none(
                    formulario.get("id_cliente"),
                    "Cliente"
                ),

            "id_motorista":
                AtendimentoService._inteiro_ou_none(
                    formulario.get("id_motorista"),
                    "Motorista"
                ),

            "id_caminhao":
                AtendimentoService._inteiro_ou_none(
                    formulario.get("id_caminhao"),
                    "Caminhão"
                ),

            "data_atendimento":
                data_atendimento,

            "protocolo": (
                formulario.get(
                    "protocolo"
                )
                or None
            ),

            "origem": (
                formulario.get(
                    "origem",
                    ""
                ).strip()
                or None
            ),

            "destino": (
                formulario.get(
                    "destino",
                    ""
                ).strip()
                or None
            ),

            "km_total":
                AtendimentoService._decimal_ou_none(
                    formulario.get(
                        "km_total"
                    )
                ),

            "valor_total": (
                AtendimentoService._decimal(
                    formulario.get(
                        "valor_total"
                    )
                )
                if formulario.get(
                    "valor_total"
                )
                else None
            ),

            "valor_pago":
                AtendimentoService._decimal(
                    formulario.get(
                        "valor_pago"
                    )
                ),

            "valor_pedagio":
                AtendimentoService._decimal(
                    formulario.get(
                        "valor_pedagio"
                    )
                ),

            "quantidade_hora_parada":
                AtendimentoService._inteiro_ou_zero(
                    formulario.get(
                        "quantidade_hora_parada"
                    )
                ),

            "quantidade_hora_trabalhada":
                AtendimentoService._inteiro_ou_zero(
                    formulario.get(
                        "quantidade_hora_trabalhada"
                    )
                ),

            "quantidade_patins":
                AtendimentoService._inteiro_ou_zero(
                    formulario.get(
                        "quantidade_patins"
                    )
                ),

            "houve_pedagio": (
                formulario.get(
                    "houve_pedagio"
                ) == "on"
            ),

            "cobrar_pedagio": (
                formulario.get(
                    "cobrar_pedagio"
                ) == "on"
            ),

            "cobrar_hora_parada": (
                formulario.get(
                    "cobrar_hora_parada"
                ) == "on"
            ),

            "cobrar_hora_trabalhada": (
                formulario.get(
                    "cobrar_hora_trabalhada"
                ) == "on"
            ),

            "usar_patins": (
                formulario.get(
                    "usar_patins"
                ) == "on"
            ),

            "placa_veiculo_rebocado":
                placa_veiculo_rebocado
                or None,

            "modelo_veiculo_rebocado":
                modelo_veiculo_rebocado
                or None,

            "pagamento_separado": (
                formulario.get(
                    "pagamento_separado"
                ) == "on"
            ),

            "observacao": (
                formulario.get(
                    "observacao"
                )
                or None
            )
        }


    # =========================================================
    # VALIDAÇÕES
    # =========================================================

    @staticmethod
    def validar(dados):

        AtendimentoService._validar_data(
            dados
        )

        AtendimentoService._validar_valores(
            dados
        )

        AtendimentoService._validar_quantidades(
            dados
        )

        AtendimentoService._validar_campos_condicionais(
            dados
        )

        AtendimentoService._validar_veiculo_rebocado(
            dados
        )


    # =========================================================
    # VALIDAÇÃO DA DATA
    # =========================================================

    @staticmethod
    def _validar_data(dados):

        data_atendimento = (
            dados["data_atendimento"]
        )

        # O atendimento pode ser criado
        # inicialmente sem data.

        if data_atendimento is None:

            return

        if data_atendimento > date.today():

            raise DataInvalidaError(
                "A data do atendimento não pode ser posterior à data atual."
            )


    # =========================================================
    # VALIDAÇÃO DOS VALORES
    # =========================================================

    @staticmethod
    def _validar_valores(dados):

        valores = {

            "km_total":
                dados["km_total"],

            "valor_total":
                dados["valor_total"],

            "valor_pago":
                dados["valor_pago"],

            "valor_pedagio":
                dados["valor_pedagio"]

        }

        for campo, valor in valores.items():

            if valor is None:

                continue

            if valor < Decimal("0"):

                raise ValorInvalidoError(

                    campo,

                    f"O valor informado para "
                    f"'{campo}' não pode ser negativo."

                )


    # =========================================================
    # VALIDAÇÃO DAS QUANTIDADES
    # =========================================================

    @staticmethod
    def _validar_quantidades(dados):

        quantidades = {

            "quantidade_hora_parada":
                dados["quantidade_hora_parada"],

            "quantidade_hora_trabalhada":
                dados["quantidade_hora_trabalhada"],

            "quantidade_patins":
                dados["quantidade_patins"]

        }

        for campo, quantidade in quantidades.items():

            if quantidade is None:

                continue

            if quantidade < 0:

                raise ValorInvalidoError(

                    campo,

                    f"A quantidade informada para "
                    f"'{campo}' não pode ser negativa."

                )


    # =========================================================
    # VALIDAÇÃO DOS CAMPOS CONDICIONAIS
    # =========================================================

    @staticmethod
    def _validar_campos_condicionais(dados):

        if (

            dados["cobrar_hora_parada"]

            and

            dados["quantidade_hora_parada"] <= 0

        ):

            raise ValorInvalidoError(

                "quantidade_hora_parada",

                (
                    "A quantidade de horas paradas "
                    "deve ser maior que zero quando "
                    "a cobrança de hora parada estiver ativa."
                )

            )


        if (

            dados["cobrar_hora_trabalhada"]

            and

            dados["quantidade_hora_trabalhada"] <= 0

        ):

            raise ValorInvalidoError(

                "quantidade_hora_trabalhada",

                (
                    "A quantidade de horas trabalhadas "
                    "deve ser maior que zero quando "
                    "a cobrança de hora trabalhada estiver ativa."
                )

            )


        if (

            dados["usar_patins"]

            and

            dados["quantidade_patins"] <= 0

        ):

            raise ValorInvalidoError(

                "quantidade_patins",

                (
                    "A quantidade de patins "
                    "deve ser maior que zero quando "
                    "o uso de patins estiver ativo."
                )

            )

        if (

            dados["houve_pedagio"]

            and

            dados["valor_pedagio"] <= 0

        ):

            raise ValorInvalidoError(

                "valor_pedagio",

                (
                    "O valor do pedágio "
                    "deve ser maior que zero quando "
                    "houve pedágio no atendimento."
                )

            )


    # =========================================================
    # VALIDAÇÃO DO VEÍCULO REBOCADO
    # =========================================================

    @staticmethod
    def _validar_veiculo_rebocado(dados):

        placa = (
            dados["placa_veiculo_rebocado"]
            or ""
        ).strip()

        # Modelo é opcional.
        # Placa também é opcional.
        #
        # Só validamos a placa quando ela
        # realmente foi informada.

        if not placa:

            return

        placa_normalizada = (
            placa
            .upper()
            .replace("-", "")
            .replace(" ", "")
        )

        import re

        placa_valida = (

            re.fullmatch(
                r"[A-Z]{3}[0-9][A-Z0-9][0-9]{2}",
                placa_normalizada
            )

            or

            re.fullmatch(
                r"[A-Z]{3}[0-9]{4}",
                placa_normalizada
            )

        )

        if not placa_valida:

            raise PlacaInvalidaError(
                placa
            )


    # =========================================================
    # VALIDAÇÃO DAS ENTIDADES
    # =========================================================

    @staticmethod
    def _validar_entidades(dados):

        administradora = Administradora.query.filter_by(
            id_administradora=dados["id_administradora"],
            ativo=True
        ).first()

        if administradora is None:

            raise RecursoNaoEncontradoError(
                "Administradora"
            )


        tipo_servico = TipoServico.query.filter_by(
            id_tipo_servico=dados["id_tipo_servico"],
            ativo=True
        ).first()

        if tipo_servico is None:

            raise RecursoNaoEncontradoError(
                "Tipo de serviço"
            )


        # -----------------------------------------------------
        # CLIENTE
        # -----------------------------------------------------

        cliente = None

        if dados["id_cliente"] is not None:

            cliente = Cliente.query.filter_by(
                id_cliente=dados["id_cliente"],
                ativo=True
            ).first()

            if cliente is None:

                raise RecursoNaoEncontradoError(
                    "Cliente"
                )

            if (
                cliente.fk_administradora_id_administradora
                != dados["id_administradora"]
            ):

                raise RegraNegocioError(
                    "O cliente selecionado não pertence "
                    "à administradora informada."
                )


        # -----------------------------------------------------
        # MOTORISTA
        # -----------------------------------------------------

        if dados["id_motorista"] is not None:

            motorista = Motorista.query.filter_by(
                id_motorista=dados["id_motorista"],
                ativo=True
            ).first()

            if motorista is None:

                raise RecursoNaoEncontradoError(
                    "Motorista"
                )


        # -----------------------------------------------------
        # CAMINHÃO
        # -----------------------------------------------------

        if dados["id_caminhao"] is not None:

            caminhao = Caminhao.query.filter_by(
                id_caminhao=dados["id_caminhao"],
                ativo=True
            ).first()

            if caminhao is None:

                raise RecursoNaoEncontradoError(
                    "Caminhão"
                )


        # -----------------------------------------------------
        # TABELA DE VALORES
        # -----------------------------------------------------

        tabela_valores = (
            TabelaValoresService.buscar_tabela(
                dados["id_administradora"],
                dados["id_tipo_servico"]
            )
        )

        if tabela_valores is None:

            raise RegraNegocioError(
                "Não existe uma tabela de valores "
                "ativa para esta administradora "
                "e tipo de serviço."
            )

        return {
            "administradora": administradora,
            "tipo_servico": tipo_servico,
            "cliente": cliente,
            "tabela_valores": tabela_valores
        }


    # =========================================================
    # VALIDAÇÃO COMPLETA
    # =========================================================

    @staticmethod
    def validar(dados):

        AtendimentoService._validar_data(
            dados
        )

        AtendimentoService._validar_valores(
            dados
        )

        AtendimentoService._validar_quantidades(
            dados
        )

        AtendimentoService._validar_campos_condicionais(
            dados
        )

        AtendimentoService._validar_veiculo_rebocado(
            dados
        )

        AtendimentoService._validar_entidades(
            dados
        )


    # =========================================================
    # DEFINIÇÃO DE STATUS
    # =========================================================

    @staticmethod
    def definir_status(dados):

        dados["status_operacional"] = (
            AtendimentoService._calcular_status_operacional(
                dados
            )
        )


        # -----------------------------------------------------
        # COMISSÃO
        # -----------------------------------------------------

        dados["valor_comissao"] = (

            (dados["valor_total"] or Decimal("0"))

            -

            (dados["valor_pedagio"] or Decimal("0"))

        )


        # -----------------------------------------------------
        # STATUS FINANCEIRO
        # -----------------------------------------------------

        valor_total = (
            dados["valor_total"]
            or Decimal("0")
        )

        valor_pago = (
            dados["valor_pago"]
            or Decimal("0")
        )


        if (

            valor_total > 0

            and

            valor_pago >= valor_total

        ):

            dados["status_financeiro"] = (
                STATUS_FINANCEIRO_PAGO
            )

        elif valor_pago > 0:

            dados["status_financeiro"] = (
                STATUS_FINANCEIRO_PAGAMENTO_PARCIAL
            )

        elif dados.get("pagamento_separado"):

            dados["status_financeiro"] = (
                STATUS_FINANCEIRO_AGUARDANDO_PAGAMENTO
            )

        else:

            dados["status_financeiro"] = (
                STATUS_FINANCEIRO_AGUARDANDO_FECHAMENTO
            )


    # =========================================================
    # STATUS OPERACIONAL
    # =========================================================

    @staticmethod
    def _calcular_status_operacional(dados):

        campos_obrigatorios = [

            dados["id_administradora"],

            dados["id_tipo_servico"],

            dados["id_cliente"],

            dados["id_motorista"],

            dados["id_caminhao"],

            dados["data_atendimento"],

            dados["protocolo"],

            dados["placa_veiculo_rebocado"],

            dados["modelo_veiculo_rebocado"],

            dados["km_total"],

            dados["valor_total"]

        ]


        if all(

            campo is not None
            and campo != ""

            for campo in campos_obrigatorios

        ):

            return STATUS_OPERACIONAL_COMPLETO


        return STATUS_OPERACIONAL_PENDENTE


    # =========================================================
    # MONTAGEM DO MODEL
    # =========================================================

    @staticmethod
    def _montar_atendimento(
        dados,
        tabela_valores,
        id_usuario
    ):

        return Atendimento(

            fk_tabela_valores_id_tabela_valores=(
                tabela_valores.id_tabela_valores
            ),

            fk_cliente_id_cliente=(
                dados["id_cliente"]
            ),

            fk_motorista_id_motorista=(
                dados["id_motorista"]
            ),

            fk_caminhao_id_caminhao=(
                dados["id_caminhao"]
            ),

            fk_usuario_id_usuario=(
                id_usuario
            ),

            data_atendimento=(
                dados["data_atendimento"]
            ),

            protocolo=(
                dados["protocolo"]
            ),

            origem=(
                dados["origem"]
            ),

            destino=(
                dados["destino"]
            ),

            km_total=(
                dados["km_total"]
            ),

            valor_total=(
                dados["valor_total"]
            ),

            valor_pago=(
                dados["valor_pago"]
            ),

            valor_pedagio=(
                dados["valor_pedagio"]
            ),

            valor_comissao=(
                dados["valor_comissao"]
            ),

            quantidade_hora_parada=(
                dados["quantidade_hora_parada"]
            ),

            quantidade_hora_trabalhada=(
                dados["quantidade_hora_trabalhada"]
            ),

            quantidade_patins=(
                dados["quantidade_patins"]
            ),

            cobrar_pedagio=(
                dados["cobrar_pedagio"]
            ),

            cobrar_hora_parada=(
                dados["cobrar_hora_parada"]
            ),

            cobrar_hora_trabalhada=(
                dados["cobrar_hora_trabalhada"]
            ),

            usar_patins=(
                dados["usar_patins"]
            ),

            observacao=(
                dados["observacao"]
            ),

            status_operacional=(
                dados["status_operacional"]
            ),

            status_financeiro=(
                dados["status_financeiro"]
            )

        )


    # =========================================================
    # VEÍCULO REBOCADO
    # =========================================================

    @staticmethod
    def _montar_veiculo_rebocado(
        atendimento,
        dados
    ):

        placa = (
            dados["placa_veiculo_rebocado"]
            or ""
        ).strip()

        modelo = (
            dados["modelo_veiculo_rebocado"]
            or ""
        ).strip()


        if not placa and not modelo:

            return None


        return VeiculoRebocado(

            atendimento=atendimento,

            placa=placa,

            modelo=modelo

        )


    @staticmethod
    def _atualizar_veiculo_rebocado(
        atendimento,
        dados
    ):

        placa = (
            dados["placa_veiculo_rebocado"]
            or ""
        ).strip()

        modelo = (
            dados["modelo_veiculo_rebocado"]
            or ""
        ).strip()


        # Nenhum veículo informado.

        if not placa and not modelo:

            if atendimento.veiculo_rebocado:

                db.session.delete(
                    atendimento.veiculo_rebocado
                )

            return


        # Ainda não existe veículo.

        if atendimento.veiculo_rebocado is None:

            atendimento.veiculo_rebocado = (
                AtendimentoService._montar_veiculo_rebocado(
                    atendimento,
                    dados
                )
            )

            return


        # Atualiza veículo existente.

        atendimento.veiculo_rebocado.placa = placa

        atendimento.veiculo_rebocado.modelo = modelo


    # =========================================================
    # SALVAR
    # =========================================================

    @staticmethod
    def salvar(
        dados,
        id_usuario
    ):

        AtendimentoService.validar(
            dados
        )

        dados["valor_comissao"] = Decimal("0.00")

        AtendimentoService.definir_status(
            dados
        )

        entidades = (
            AtendimentoService._validar_entidades(
                dados
            )
        )

        tabela_valores = (
            entidades["tabela_valores"]
        )

        atendimento = (
            AtendimentoService._montar_atendimento(

                dados=dados,

                tabela_valores=tabela_valores,

                id_usuario=id_usuario

            )
        )

        db.session.add(
            atendimento
        )

        db.session.flush()

        veiculo_rebocado = (
            AtendimentoService._montar_veiculo_rebocado(

                atendimento,

                dados

            )
        )

        if veiculo_rebocado:

            db.session.add(
                veiculo_rebocado
            )

        db.session.commit()

        return atendimento


    # =========================================================
    # ATUALIZAR
    # =========================================================

    @staticmethod
    def atualizar(
        atendimento,
        dados
    ):

        AtendimentoService.validar(
            dados
        )

        AtendimentoService.definir_status(
            dados
        )

        entidades = (
            AtendimentoService._validar_entidades(
                dados
            )
        )

        tabela_valores = (
            entidades["tabela_valores"]
        )

        atendimento.fk_tabela_valores_id_tabela_valores = (
            tabela_valores.id_tabela_valores
        )

        atendimento.fk_cliente_id_cliente = (
            dados["id_cliente"]
        )

        atendimento.fk_motorista_id_motorista = (
            dados["id_motorista"]
        )

        atendimento.fk_caminhao_id_caminhao = (
            dados["id_caminhao"]
        )

        atendimento.data_atendimento = (
            dados["data_atendimento"]
        )

        atendimento.protocolo = (
            dados["protocolo"]
        )

        atendimento.origem = (
            dados["origem"]
        )

        atendimento.destino = (
            dados["destino"]
        )

        atendimento.km_total = (
            dados["km_total"]
        )

        atendimento.valor_total = (
            dados["valor_total"]
        )

        atendimento.valor_pago = (
            dados["valor_pago"]
        )

        atendimento.valor_pedagio = (
            dados["valor_pedagio"]
        )

        atendimento.valor_comissao = (
            dados["valor_comissao"]
        )

        atendimento.quantidade_hora_parada = (
            dados["quantidade_hora_parada"]
        )

        atendimento.quantidade_hora_trabalhada = (
            dados["quantidade_hora_trabalhada"]
        )

        atendimento.quantidade_patins = (
            dados["quantidade_patins"]
        )

        atendimento.cobrar_pedagio = (
            dados["cobrar_pedagio"]
        )

        atendimento.cobrar_hora_parada = (
            dados["cobrar_hora_parada"]
        )

        atendimento.cobrar_hora_trabalhada = (
            dados["cobrar_hora_trabalhada"]
        )

        atendimento.usar_patins = (
            dados["usar_patins"]
        )

        atendimento.status_operacional = (
            dados["status_operacional"]
        )

        atendimento.status_financeiro = (
            dados["status_financeiro"]
        )

        atendimento.observacao = (
            dados["observacao"]
        )

        AtendimentoService._atualizar_veiculo_rebocado(
            atendimento,
            dados
        )

        db.session.commit()

        return atendimento


    # =========================================================
    # EXCLUIR
    # =========================================================

    @staticmethod
    def excluir(
        id_atendimento
    ):

        atendimento = (
            AtendimentoService.detalhes(
                id_atendimento
            )
        )


        db.session.delete(
            atendimento
        )

        db.session.commit()


    # =========================================================
    # REGISTRAR PAGAMENTO
    # =========================================================

    @staticmethod
    def registrar_pagamento(
        atendimentos,
        commit=True
    ):

        for atendimento in atendimentos:

            if (
                atendimento.valor_total is None
                or
                atendimento.valor_total <= 0
            ):

                raise ValorInvalidoError(

                    "valor_total",

                    (
                        "Não é possível registrar "
                        "o pagamento de um atendimento "
                        "sem valor total válido."
                    )

                )


            atendimento.valor_pago = (
                atendimento.valor_total
            )

            atendimento.status_financeiro = (
                STATUS_FINANCEIRO_PAGO
            )


        if commit:

            db.session.commit()


    # =========================================================
    # FORMULÁRIO
    # =========================================================

    @staticmethod
    def carregar_formulario():

        return {

            "administradoras":
                Administradora.query
                    .join(
                        TabelaValores,
                        TabelaValores.fk_administradora_id_administradora
                        == Administradora.id_administradora
                    )
                    .join(
                        Cliente,
                        Cliente.fk_administradora_id_administradora
                        == Administradora.id_administradora
                    )
                    .filter(
                        Administradora.ativo.is_(True),
                        TabelaValores.ativo.is_(True),
                        Cliente.ativo.is_(True)
                    )
                    .distinct()
                    .order_by(
                        Administradora.nome
                    )
                    .all(),

            "tipos_servico":
                TipoServico.query.filter_by(
                    ativo=True
                ).order_by(
                    TipoServico.nome
                ).all(),

            "clientes":
                Cliente.query.filter_by(
                    ativo=True
                ).order_by(
                    Cliente.nome_fantasia
                ).all(),

            "motoristas":
                Motorista.query.filter_by(
                    ativo=True
                ).order_by(
                    Motorista.nome
                ).all(),

            "caminhoes":
                Caminhao.query.filter_by(
                    ativo=True
                ).order_by(
                    Caminhao.placa
                ).all()

        }


    # =========================================================
    # LISTAGEM
    # =========================================================

    @staticmethod
    def listar(filtros=None):

        if filtros is not None:

            return FilterService.listar(

                modelo=Atendimento,

                filtros=filtros,

                configuracoes=FILTROS_ATENDIMENTO,

                ordenar_por="data_atendimento"

            )


        return (

            Atendimento.query

            .options(

                joinedload(
                    Atendimento.cliente
                ),

                joinedload(
                    Atendimento.usuario
                ),

                joinedload(
                    Atendimento.motorista
                ),

                joinedload(
                    Atendimento.caminhao
                ),

                joinedload(
                    Atendimento.tabela_valores
                ).joinedload(
                    TabelaValores.administradora
                ),

                joinedload(
                    Atendimento.tabela_valores
                ).joinedload(
                    TabelaValores.tipo_servico
                ),

                joinedload(
                    Atendimento.veiculo_rebocado
                )

            )

            .order_by(

                Atendimento.data_cadastro.desc(),

                Atendimento.id_atendimento.desc()

            )

            .all()

        )


    # =========================================================
    # DETALHES
    # =========================================================

    @staticmethod
    def detalhes(
        id_atendimento
    ):

        atendimento = Atendimento.query.get(
            id_atendimento
        )

        if atendimento is None:

            raise RecursoNaoEncontradoError(
                "Atendimento"
            )

        return atendimento


    # =========================================================
    # VISUALIZAÇÃO COMPLETA
    # =========================================================

    @staticmethod
    def listar_completo(
        filtros
    ):

        return FilterService.listar(

            modelo=Atendimento,

            filtros=filtros,

            configuracoes=FILTROS_ATENDIMENTO,

            ordenar_por="data_cadastro"

        )


    # =========================================================
    # TABELA DE VALORES
    # =========================================================

    @staticmethod
    def buscar_tabela_valores(
        id_administradora,
        id_tipo_servico
    ):

        if (
            not id_administradora
            or
            not id_tipo_servico
        ):

            return None


        return (
            TabelaValoresService.buscar_tabela(

                id_administradora,

                id_tipo_servico

            )
        )


    # =========================================================
    # GOOGLE MAPS
    # =========================================================

    @staticmethod
    def _calcular_distancia(
        origem,
        destino
    ):

        return GoogleMapsService.calcular_distancia(

            origem,

            destino

        )


    @staticmethod
    def calcular_distancia(
        origem,
        destino
    ):

        if not origem or not str(origem).strip():

            raise CampoObrigatorioError(
                "origem"
            )


        if not destino or not str(destino).strip():

            raise CampoObrigatorioError(
                "destino"
            )


        try:

            return AtendimentoService._calcular_distancia(

                origem.strip(),

                destino.strip()

            )

        except Exception as erro:

            raise RegraNegocioError(
                str(erro)
            )