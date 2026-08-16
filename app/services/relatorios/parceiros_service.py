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
    def gerar_relatorio_por_cliente(

        id_administradora,

        data_inicial: date,

        data_final: date

    ):

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

            .join(
                Atendimento,
                Atendimento.fk_cliente_id_cliente
                == Cliente.id_cliente
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

            .filter(
                Atendimento.data_atendimento
                >= data_inicial
            )

            .filter(
                Atendimento.data_atendimento
                <= data_final
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
                    / km_total
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
                / km_total
            )

        else:

            valor_medio_por_km_total = None

        administradora = Administradora.query.get_or_404(
            id_administradora
        )

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