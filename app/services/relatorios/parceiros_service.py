from datetime import date
from decimal import Decimal

from sqlalchemy import func

from app import db
from app.models import (
    Administradora,
    Atendimento,
    Cliente,
    TabelaValores
)

from app.constants.atendimento import (
    STATUS_FINANCEIRO_AGUARDANDO_FECHAMENTO,
    STATUS_FINANCEIRO_PAGO
)

class ParceirosRelatorioService:

    @staticmethod
    def gerar_relatorio(
        data_inicial: date,
        data_final: date
    ):

        resultados = (

            db.session.query(

                Administradora.id_administradora,

                Administradora.nome,

                func.coalesce(
                    func.sum(
                        Atendimento.valor_total
                    ),
                    0
                ).label(
                    "faturamento_bruto"
                ),

                func.coalesce(
                    func.sum(
                        Atendimento.km_total
                    ),
                    0
                ).label(
                    "km_total"
                ),

                func.count(
                    Atendimento.id_atendimento
                ).label(
                    "quantidade_atendimentos"
                )

            )

            .outerjoin(
                TabelaValores,
                TabelaValores.fk_administradora_id_administradora
                == Administradora.id_administradora
            )

            .outerjoin(
                Atendimento,
                db.and_(

                    Atendimento.fk_tabela_valores_id_tabela_valores
                    == TabelaValores.id_tabela_valores,

                    Atendimento.data_atendimento
                    >= data_inicial,

                    Atendimento.data_atendimento
                    <= data_final

                )
            )

            .filter(
                Administradora.ativo.is_(True)
            )

            .group_by(
                Administradora.id_administradora,
                Administradora.nome
            )

            .order_by(
                Administradora.nome.asc()
            )

            .all()

        )

        parceiros = []

        for resultado in resultados:

            faturamento_bruto = Decimal(
                str(
                    resultado.faturamento_bruto
                )
            )

            km_total = Decimal(
                str(
                    resultado.km_total
                )
            )

            if km_total != 0:

                valor_medio_por_km = (
                    faturamento_bruto
                    / km_total
                )

            else:

                valor_medio_por_km = None

            parceiros.append({

                "id_administradora":
                    resultado.id_administradora,

                "nome":
                    resultado.nome,

                "faturamento_bruto":
                    faturamento_bruto,

                "km_total":
                    km_total,

                "quantidade_atendimentos":
                    resultado.quantidade_atendimentos,

                "valor_medio_por_km":
                    valor_medio_por_km

            })

        faturamento_total = sum(

            parceiro["faturamento_bruto"]

            for parceiro in parceiros

        )

        km_total = sum(

            parceiro["km_total"]

            for parceiro in parceiros

        )

        quantidade_atendimentos_total = sum(

            parceiro["quantidade_atendimentos"]

            for parceiro in parceiros

        )

        if km_total != 0:

            valor_medio_por_km_total = (
                faturamento_total
                / km_total
            )

        else:

            valor_medio_por_km_total = None

        return {

            "parceiros":
                parceiros,

            "faturamento_total":
                faturamento_total,

            "km_total":
                km_total,

            "quantidade_atendimentos_total":
                quantidade_atendimentos_total,

            "valor_medio_por_km_total":
                valor_medio_por_km_total

        }

    @staticmethod
    def buscar_detalhes(
        id_administradora,
        data_inicial,
        data_final
    ):

        administradora = Administradora.query.get_or_404(
            id_administradora
        )

        query = (

            Atendimento.query

            .join(

                TabelaValores,

                TabelaValores.id_tabela_valores
                ==
                Atendimento.fk_tabela_valores_id_tabela_valores

            )

            .filter(

                TabelaValores.fk_administradora_id_administradora
                ==
                id_administradora

            )

            .filter(

                Atendimento.data_atendimento
                >= data_inicial

            )

            .filter(

                Atendimento.data_atendimento
                <= data_final

            )

            .order_by(

                Atendimento.data_atendimento.asc(),

                Atendimento.id_atendimento.asc()

            )

        )

        return administradora, query.all()

    @staticmethod
    def gerar_relatorio_por_cliente(

        id_administradora,

        data_inicial,

        data_final

    ):

        administradora = Administradora.query.get_or_404(

            id_administradora

        )

        # =====================================================
        # CLIENTES QUE JÁ POSSUEM RELAÇÃO COM A ADMINISTRADORA
        # =====================================================

        clientes_relacionados = (

            db.session.query(

                Atendimento.fk_cliente_id_cliente

            )

            .join(

                TabelaValores,

                TabelaValores.id_tabela_valores
                == Atendimento.fk_tabela_valores_id_tabela_valores

            )

            .filter(

                TabelaValores.fk_administradora_id_administradora
                == id_administradora

            )

            .distinct()

            .subquery()

        )


        # =====================================================
        # RELATÓRIO
        # =====================================================

        resultados = (

            db.session.query(

                Cliente.id_cliente,

                Cliente.nome_fantasia,

                func.coalesce(

                    func.sum(
                        Atendimento.valor_total
                    ),

                    0

                ).label(

                    "faturamento_bruto"

                ),

                func.coalesce(

                    func.sum(
                        Atendimento.km_total
                    ),

                    0

                ).label(

                    "km_total"

                ),

                func.count(

                    Atendimento.id_atendimento

                ).label(

                    "quantidade_atendimentos"

                )

            )

            .outerjoin(

                Atendimento,

                db.and_(

                    Atendimento.fk_cliente_id_cliente
                    == Cliente.id_cliente,

                    Atendimento.data_atendimento
                    >= data_inicial,

                    Atendimento.data_atendimento
                    <= data_final,

                    Atendimento.fk_tabela_valores_id_tabela_valores.in_(

                        db.session.query(

                            TabelaValores.id_tabela_valores

                        ).filter(

                            TabelaValores.fk_administradora_id_administradora
                            == id_administradora

                        )

                    )

                )

            )

            .filter(

                Cliente.ativo.is_(True)

            )

            .filter(

                Cliente.id_cliente.in_(

                    db.session.query(

                        clientes_relacionados.c.fk_cliente_id_cliente

                    )

                )

            )

            .group_by(

                Cliente.id_cliente,

                Cliente.nome_fantasia

            )

            .order_by(

                Cliente.nome_fantasia.asc()

            )

            .all()

        )


        # =====================================================
        # FORMATAÇÃO
        # =====================================================

        clientes = []

        for resultado in resultados:

            faturamento_bruto = Decimal(

                str(
                    resultado.faturamento_bruto
                )

            )

            km_total = Decimal(

                str(
                    resultado.km_total
                )

            )

            if km_total != 0:

                valor_medio_por_km = (

                    faturamento_bruto
                    /
                    km_total

                )

            else:

                valor_medio_por_km = None

            clientes.append({

                "id_cliente":
                    resultado.id_cliente,

                "nome":
                    resultado.nome_fantasia,

                "faturamento_bruto":
                    faturamento_bruto,

                "km_total":
                    km_total,

                "quantidade_atendimentos":
                    resultado.quantidade_atendimentos,

                "valor_medio_por_km":
                    valor_medio_por_km

            })


        # =====================================================
        # TOTAIS
        # =====================================================

        faturamento_total = sum(

            cliente["faturamento_bruto"]

            for cliente in clientes

        )

        km_total = sum(

            cliente["km_total"]

            for cliente in clientes

        )

        quantidade_atendimentos_total = sum(

            cliente["quantidade_atendimentos"]

            for cliente in clientes

        )

        if km_total != 0:

            valor_medio_por_km_total = (

                faturamento_total
                /
                km_total

            )

        else:

            valor_medio_por_km_total = None


        return {

            "administradora":
                administradora,

            "clientes":
                clientes,

            "faturamento_total":
                faturamento_total,

            "km_total":
                km_total,

            "quantidade_atendimentos_total":
                quantidade_atendimentos_total,

            "valor_medio_por_km_total":
                valor_medio_por_km_total

        }

    @staticmethod
    def buscar_detalhes_cliente(
        id_administradora,
        id_cliente,
        data_inicial,
        data_final
    ):

        administradora = Administradora.query.get_or_404(
            id_administradora
        )

        cliente = Cliente.query.get_or_404(
            id_cliente
        )

        query = (

            Atendimento.query

            .join(
                TabelaValores,
                TabelaValores.id_tabela_valores
                ==
                Atendimento.fk_tabela_valores_id_tabela_valores
            )

            .filter(
                TabelaValores.fk_administradora_id_administradora
                == id_administradora
            )

            .filter(
                Atendimento.fk_cliente_id_cliente
                == id_cliente
            )

            .filter(
                Atendimento.data_atendimento
                >= data_inicial
            )

            .filter(
                Atendimento.data_atendimento
                <= data_final
            )

            .order_by(
                Atendimento.data_atendimento.asc(),
                Atendimento.id_atendimento.asc()
            )

        )

        return (
            administradora,
            cliente,
            query.all()
        )

    @staticmethod
    def buscar_atendimentos_para_fechamento(
        id_administradora,
        id_cliente,
        data_inicial,
        data_final
    ):

        administradora = Administradora.query.get_or_404(
            id_administradora
        )

        cliente = Cliente.query.get_or_404(
            id_cliente
        )

        query = (

            Atendimento.query

            .join(
                TabelaValores,
                TabelaValores.id_tabela_valores
                ==
                Atendimento.fk_tabela_valores_id_tabela_valores
            )

            .filter(
                TabelaValores.fk_administradora_id_administradora
                == id_administradora
            )

            .filter(
                Atendimento.fk_cliente_id_cliente
                == id_cliente
            )

            .filter(
                Atendimento.data_atendimento
                >= data_inicial
            )

            .filter(
                Atendimento.data_atendimento
                <= data_final
            )

            .filter(
                Atendimento.status_financeiro
                == STATUS_FINANCEIRO_AGUARDANDO_FECHAMENTO
            )

            .order_by(
                Atendimento.data_atendimento.asc(),
                Atendimento.id_atendimento.asc()
            )

        )

        return (
            administradora,
            cliente,
            query.all()
        )


    @staticmethod
    def realizar_fechamento(
        id_administradora,
        id_cliente,
        data_inicial,
        data_final
    ):

        atendimentos = (

            Atendimento.query

            .join(
                TabelaValores,
                TabelaValores.id_tabela_valores
                ==
                Atendimento.fk_tabela_valores_id_tabela_valores
            )

            .filter(
                TabelaValores.fk_administradora_id_administradora
                == id_administradora
            )

            .filter(
                Atendimento.fk_cliente_id_cliente
                == id_cliente
            )

            .filter(
                Atendimento.data_atendimento
                >= data_inicial
            )

            .filter(
                Atendimento.data_atendimento
                <= data_final
            )

            .filter(
                Atendimento.status_financeiro
                == STATUS_FINANCEIRO_AGUARDANDO_FECHAMENTO
            )

            .all()

        )

        quantidade = len(
            atendimentos
        )

        for atendimento in atendimentos:

            atendimento.status_financeiro = (
                STATUS_FINANCEIRO_PAGO
            )

        db.session.commit()

        return quantidade
    
    @staticmethod
    def listar_para_exportacao(parametros):

        data_inicial = parametros.get(
            "data_inicial"
        )

        data_final = parametros.get(
            "data_final"
        )

        hoje = date.today()

        if not data_inicial:

            data_inicial = (
                f"{hoje.year:04d}-"
                f"{hoje.month:02d}-01"
            )

        if not data_final:

            data_final = hoje.isoformat()

        data_inicial = date.fromisoformat(
            data_inicial
        )

        data_final = date.fromisoformat(
            data_final
        )

        return ParceirosRelatorioService.gerar_relatorio(
            data_inicial,
            data_final
        )
    
    @staticmethod
    def listar_clientes_para_exportacao(filtros):

        id_administradora = filtros.get(
            "id_administradora",
            type=int
        )

        data_inicial_texto = filtros.get(
            "data_inicial"
        )

        data_final_texto = filtros.get(
            "data_final"
        )

        if (
            not id_administradora
            or not data_inicial_texto
            or not data_final_texto
        ):

            return []

        try:

            data_inicial = date.fromisoformat(
                data_inicial_texto
            )

            data_final = date.fromisoformat(
                data_final_texto
            )

        except ValueError:

            return []

        resultado = (
            ParceirosRelatorioService.gerar_relatorio_por_cliente(

                id_administradora,

                data_inicial,

                data_final

            )
        )

        return resultado["clientes"]

    @staticmethod
    def listar_detalhes_cliente_para_exportacao(
        parametros
    ):

        id_administradora = parametros.get(
            "id_administradora",
            type=int
        )

        id_cliente = parametros.get(
            "id_cliente",
            type=int
        )

        data_inicial_texto = parametros.get(
            "data_inicial"
        )

        data_final_texto = parametros.get(
            "data_final"
        )

        if (
            not id_administradora
            or not id_cliente
            or not data_inicial_texto
            or not data_final_texto
        ):

            return []

        try:

            data_inicial = date.fromisoformat(
                data_inicial_texto
            )

            data_final = date.fromisoformat(
                data_final_texto
            )

        except ValueError:

            return []

        (
            administradora,
            cliente,
            atendimentos
        ) = ParceirosRelatorioService.buscar_detalhes_cliente(

            id_administradora,

            id_cliente,

            data_inicial,

            data_final

        )

        dados = []

        for atendimento in atendimentos:

            if atendimento.caminhao:

                caminhao = (

                    f"{atendimento.caminhao.modelo}"
                    f" - "
                    f"{atendimento.caminhao.placa}"

                )

            else:

                caminhao = "—"

            dados.append({

                "data_atendimento":
                    atendimento.data_atendimento,

                "cliente":
                    (
                        atendimento.cliente.nome_fantasia
                        if atendimento.cliente
                        else "—"
                    ),

                "motorista":
                    (
                        atendimento.motorista.nome
                        if atendimento.motorista
                        else "—"
                    ),

                "caminhao":
                    caminhao,

                "tipo_servico":
                    (
                        atendimento.tabela_valores
                        .tipo_servico
                        .nome
                        if (
                            atendimento.tabela_valores
                            and
                            atendimento.tabela_valores.tipo_servico
                        )
                        else "—"
                    ),

                "km_total":
                    atendimento.km_total,

                "valor_total":
                    atendimento.valor_total

            })

        return dados

    @staticmethod
    def listar_detalhes_para_exportacao(parametros):

        id_administradora = parametros.get(
            "id_administradora",
            type=int
        )

        data_inicial_texto = parametros.get(
            "data_inicial"
        )

        data_final_texto = parametros.get(
            "data_final"
        )

        if (
            not id_administradora
            or not data_inicial_texto
            or not data_final_texto
        ):

            return []

        try:

            data_inicial = date.fromisoformat(
                data_inicial_texto
            )

            data_final = date.fromisoformat(
                data_final_texto
            )

        except ValueError:

            return []

        administradora, atendimentos = (
            ParceirosRelatorioService.buscar_detalhes(
                id_administradora,
                data_inicial,
                data_final
            )
        )

        dados = []

        for atendimento in atendimentos:

            if atendimento.caminhao:

                caminhao = (
                    f"{atendimento.caminhao.modelo}"
                    f" - "
                    f"{atendimento.caminhao.placa}"
                )

            else:

                caminhao = "—"

            dados.append({

                "data_atendimento":
                    atendimento.data_atendimento,

                "cliente":
                    (
                        atendimento.cliente.nome_fantasia
                        if atendimento.cliente
                        else "—"
                    ),

                "motorista":
                    (
                        atendimento.motorista.nome
                        if atendimento.motorista
                        else "—"
                    ),

                "caminhao":
                    caminhao,

                "tipo_servico":
                    (
                        atendimento.tabela_valores
                        .tipo_servico
                        .nome
                        if (
                            atendimento.tabela_valores
                            and
                            atendimento.tabela_valores.tipo_servico
                        )
                        else "—"
                    ),

                "km_total":
                    atendimento.km_total,

                "valor_total":
                    atendimento.valor_total

            })

        return dados

    @staticmethod
    def listar_para_exportacao(parametros):

        data_inicial_texto = parametros.get(
            "data_inicial"
        )

        data_final_texto = parametros.get(
            "data_final"
        )

        if not data_inicial_texto or not data_final_texto:

            return []

        try:

            data_inicial = date.fromisoformat(
                data_inicial_texto
            )

            data_final = date.fromisoformat(
                data_final_texto
            )

        except ValueError:

            return []

        resultado = (
            ParceirosRelatorioService.gerar_relatorio(
                data_inicial,
                data_final
            )
        )

        return resultado.get(
            "parceiros",
            []
        )