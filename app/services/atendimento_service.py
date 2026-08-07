from datetime import date
from decimal import Decimal
from sqlalchemy.orm import joinedload

from app import db

from app.models import (
    Atendimento,
    Administradora,
    TipoServico,
    Cliente,
    Motorista,
    Caminhao, 
    VeiculoRebocado, 
    TabelaValores
)

from app.services.tabela_valores_service import (
    TabelaValoresService
)
from app.services.filter_service import (
    FilterService
)
from app.services.google_maps_service import (
    GoogleMapsService
)

from app.filters.atendimento import (
    FILTROS_ATENDIMENTO
)

from app.constants.atendimento import (
    KM_FRANQUIA,
    VALOR_PATINS,
    VALOR_HORA_PARADA,
    VALOR_HORA_TRABALHADA,
    STATUS_OPERACIONAL_PENDENTE,
    STATUS_OPERACIONAL_COMPLETO,
    STATUS_FINANCEIRO_AGUARDANDO_PAGAMENTO,
    STATUS_FINANCEIRO_PAGAMENTO_PARCIAL,
    STATUS_FINANCEIRO_PAGO
)


class AtendimentoService:

    @staticmethod
    def _decimal(valor):

        return Decimal(valor or "0")

    @staticmethod
    def _inteiro(valor):

        return int(valor) if valor else 0

    @staticmethod
    def _inteiro_ou_none(valor):

        return int(valor) if valor else None

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

            ),

        )

    @staticmethod
    def _montar_veiculo_rebocado(

        atendimento,

        dados

    ):

        if (

            not dados["placa_veiculo_rebocado"]

            and

            not dados["modelo_veiculo_rebocado"]

        ):

            return None

        return VeiculoRebocado(

            atendimento=atendimento,

            placa=dados["placa_veiculo_rebocado"],

            modelo=dados["modelo_veiculo_rebocado"]

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

        if not placa and not modelo:

            if atendimento.veiculo_rebocado:

                db.session.delete(

                    atendimento.veiculo_rebocado

                )

            return

        if atendimento.veiculo_rebocado is None:

            atendimento.veiculo_rebocado = (

                AtendimentoService._montar_veiculo_rebocado(

                    atendimento,

                    dados

                )

            )

            return

        atendimento.veiculo_rebocado.placa = placa

        atendimento.veiculo_rebocado.modelo = modelo

    @staticmethod
    def excluir(
        id_atendimento
    ):

        atendimento = AtendimentoService.detalhes(

            id_atendimento

        )

        db.session.delete(

            atendimento

        )

        db.session.commit()

    @staticmethod
    def montar_dados(formulario):

        return {

            "id_administradora": AtendimentoService._inteiro(
                formulario.get("id_administradora")
            ),

            "id_tipo_servico": AtendimentoService._inteiro(
                formulario.get("id_tipo_servico")
            ),

            "id_cliente": AtendimentoService._inteiro_ou_none(
                formulario.get("id_cliente")
            ),

            "id_motorista": AtendimentoService._inteiro_ou_none(
                formulario.get("id_motorista")
            ),

            "id_caminhao": AtendimentoService._inteiro_ou_none(
                formulario.get("id_caminhao")
            ),

            "data_atendimento": (

                date.fromisoformat(
                    formulario["data_atendimento"]
                )

                if formulario.get(
                    "data_atendimento"
                )

                else None

            ),

            "protocolo": (
                formulario.get("protocolo")
                or None
            ),

            "origem": formulario.get(
                "origem",
                ""
            ).strip() or None,

            "destino": formulario.get(
                "destino",
                ""
            ).strip() or None,

            "km_total": AtendimentoService._decimal(
                formulario.get("km_total")
            ),

            "valor_total": (

                AtendimentoService._decimal(
                    formulario.get("valor_total")
                )

                if formulario.get(
                    "valor_total"
                )

                else None

            ),

            "valor_pago": AtendimentoService._decimal(
                formulario.get("valor_pago")
            ),

            "valor_pedagio": AtendimentoService._decimal(
                formulario.get("valor_pedagio")
            ),

            "quantidade_hora_parada": AtendimentoService._inteiro(
                formulario.get(
                    "quantidade_hora_parada"
                )
            ),

            "quantidade_hora_trabalhada": AtendimentoService._inteiro(
                formulario.get(
                    "quantidade_hora_trabalhada"
                )
            ),

            "quantidade_patins": AtendimentoService._inteiro(
                formulario.get("quantidade_patins")
            ),

            "cobrar_pedagio": (
                formulario.get("cobrar_pedagio")
                == "on"
            ),

            "cobrar_hora_parada": (
                formulario.get("cobrar_hora_parada")
                == "on"
            ),

            "cobrar_hora_trabalhada": (
                formulario.get("cobrar_hora_trabalhada")
                == "on"
            ),

            "usar_patins": (
                formulario.get("usar_patins")
                == "on"
            ),

            "placa_veiculo_rebocado": (
                formulario.get("placa_veiculo_rebocado")
                or None
            ),

            "modelo_veiculo_rebocado": (

                formulario.get("modelo_veiculo_rebocado")
                or None
            ),

            "observacao": (
                formulario.get("observacao")
                or None
            )

        }

    @staticmethod
    def salvar(
        dados,
        id_usuario
    ):

        tabela_valores = (

            TabelaValoresService.buscar_tabela(

                dados["id_administradora"],

                dados["id_tipo_servico"]

            )

        )

        if tabela_valores is None:

            raise ValueError(

                "Não existe uma tabela de valores ativa para esta administradora e tipo de serviço."

            )

        AtendimentoService.definir_status(

            dados

        )

        atendimento = AtendimentoService._montar_atendimento(

            dados=dados,

            tabela_valores=tabela_valores,

            id_usuario=id_usuario

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

    @staticmethod
    def atualizar(

        atendimento,

        dados

    ):

        tabela_valores = (

            TabelaValoresService.buscar_tabela(

                dados["id_administradora"],

                dados["id_tipo_servico"]

            )

        )

        if tabela_valores is None:

            raise ValueError(

                "Não existe uma tabela de valores ativa para esta administradora e tipo de serviço."

            )

        AtendimentoService.definir_status(

            dados

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

    @staticmethod
    def carregar_formulario():

        return {

            "administradoras": Administradora.query.filter_by(
                ativo=True
            ).order_by(
                Administradora.nome
            ).all(),

            "tipos_servico": TipoServico.query.filter_by(
                ativo=True
            ).order_by(
                TipoServico.nome
            ).all(),

            "clientes": Cliente.query.filter_by(
                ativo=True
            ).order_by(
                Cliente.nome_fantasia
            ).all(),

            "motoristas": Motorista.query.filter_by(
                ativo=True
            ).order_by(
                Motorista.nome
            ).all(),

            "caminhoes": Caminhao.query.filter_by(
                ativo=True
            ).order_by(
                Caminhao.placa
            ).all()

        }

    @staticmethod
    def listar():

        return (

            Atendimento.query

            .options(

                joinedload(Atendimento.cliente),

                joinedload(Atendimento.usuario),

                joinedload(Atendimento.motorista),

                joinedload(Atendimento.caminhao),

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

    @staticmethod
    def detalhes(id_atendimento):

        return Atendimento.query.get_or_404(

            id_atendimento

        )

    @staticmethod
    def listar_completo(filtros):

        atendimentos = FilterService.listar(

            modelo=Atendimento,

            filtros=filtros,

            configuracoes=FILTROS_ATENDIMENTO,

            ordenar_por="data_cadastro"

        )

        return atendimentos

    # Futuramente será aplicado aqui o filtro
    # por Administradora utilizando a TabelaValores.

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

        return TabelaValoresService.buscar_tabela(

            id_administradora,

            id_tipo_servico

        )

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

        try:

            return AtendimentoService._calcular_distancia(

                origem,

                destino

            )

        except Exception as erro:

            raise ValueError(

                str(erro)

            )

    @staticmethod
    def definir_status(dados):

        dados["status_operacional"] = (

            AtendimentoService._calcular_status_operacional(

                dados

            )

        )

        if dados["valor_pago"] <= 0:

            dados["status_financeiro"] = (

                STATUS_FINANCEIRO_AGUARDANDO_PAGAMENTO

            )

        elif dados["valor_pago"] < dados["valor_total"]:

            dados["status_financeiro"] = (

                STATUS_FINANCEIRO_PAGAMENTO_PARCIAL

            )

        else:

            dados["status_financeiro"] = (

                STATUS_FINANCEIRO_PAGO

            )

    @staticmethod
    def _calcular_status_operacional(
        dados
    ):

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

        if all(campos_obrigatorios):

            return STATUS_OPERACIONAL_COMPLETO

        return STATUS_OPERACIONAL_PENDENTE