from datetime import date
from decimal import Decimal

from sqlalchemy import func

from app import db
from app.models import Motorista, Atendimento

from app.constants.motorista import COMISSAO_MOTORISTA

class MotoristasRelatorioService:

    @staticmethod
    def gerar_relatorio(
        data_inicial: date,
        data_final: date
    ):

        resultados = (

            db.session.query(

                Motorista.id_motorista,

                Motorista.nome,

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
                ),

                func.coalesce(
                    func.sum(
                        Atendimento.valor_comissao
                    ),
                    0
                ).label(
                    "valor_antes_comissao"
                )

            )

            .outerjoin(
                Atendimento,
                db.and_(
                    Atendimento.fk_motorista_id_motorista
                    == Motorista.id_motorista,

                    Atendimento.data_atendimento
                    >= data_inicial,

                    Atendimento.data_atendimento
                    <= data_final
                )
            )

            .filter(
                Motorista.ativo.is_(True)
            )

            .group_by(
                Motorista.id_motorista,
                Motorista.nome
            )

            .order_by(
                Motorista.nome.asc()
            )

            .all()

        )

        resultados_formatados = []

        for resultado in resultados:

            valor_antes_comissao = (
                Decimal(
                    str(
                        resultado.valor_antes_comissao
                    )
                )
            )

            valor_comissao = (
                valor_antes_comissao
                * COMISSAO_MOTORISTA
            )

            resultados_formatados.append({

                "id_motorista":
                    resultado.id_motorista,

                "nome":
                    resultado.nome,

                "faturamento_bruto":
                    resultado.faturamento_bruto,

                "km_total":
                    resultado.km_total,

                "quantidade_atendimentos":
                    resultado.quantidade_atendimentos,

                "valor_comissao":
                    valor_comissao

            })

        faturamento_total = sum(

            resultado["faturamento_bruto"]

            for resultado in resultados_formatados

        )

        quantidade_atendimentos_total = sum(

            resultado["quantidade_atendimentos"]

            for resultado in resultados_formatados

        )

        km_total = sum(

            resultado["km_total"]

            for resultado in resultados_formatados

        )

        valor_comissao_total = sum(

            resultado["valor_comissao"]

            for resultado in resultados_formatados

        )

        return {

            "motoristas":
                resultados_formatados,

            "faturamento_total":
                faturamento_total,

            "quantidade_atendimentos_total":
                quantidade_atendimentos_total,

            "km_total":
                km_total,

            "valor_comissao_total":
                valor_comissao_total

        }

    @staticmethod
    def buscar_detalhes(
        id_motorista,
        data_inicial,
        data_final
    ):

        query = (

            Atendimento.query

            .filter(
                Atendimento.fk_motorista_id_motorista
                == id_motorista
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

        return query.all()

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

        return MotoristasRelatorioService.gerar_relatorio(
            data_inicial,
            data_final
        )