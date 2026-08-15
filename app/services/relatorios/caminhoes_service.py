from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app import db
from app.models import Caminhao, Atendimento, TabelaValores


class CaminhoesRelatorioService:

    @staticmethod
    def gerar_relatorio(
        data_inicial: date,
        data_final: date
    ):

        resultados = (

            db.session.query(

                Caminhao.id_caminhao,

                Caminhao.modelo,

                Caminhao.placa,

                func.coalesce(
                    func.sum(Atendimento.valor_total),
                    0
                ).label("faturamento_bruto"),

                func.coalesce(
                    func.sum(Atendimento.km_total),
                    0
                ).label("km_total"),

                func.count(
                    Atendimento.id_atendimento
                ).label("quantidade_atendimentos")

            )

            .outerjoin(
                Atendimento,
                Atendimento.fk_caminhao_id_caminhao
                == Caminhao.id_caminhao
            )

            .filter(
                Caminhao.ativo.is_(True)
            )

            .filter(
                db.or_(
                    Atendimento.id_atendimento.is_(None),

                    db.and_(
                        Atendimento.data_atendimento
                        >= data_inicial,

                        Atendimento.data_atendimento
                        <= data_final
                    )
                )
            )

            .group_by(
                Caminhao.id_caminhao,
                Caminhao.modelo,
                Caminhao.placa
            )

            .order_by(
                Caminhao.modelo.asc(),
                Caminhao.placa.asc()
            )

            .all()

        )

        faturamento_total = sum(
            resultado.faturamento_bruto
            for resultado in resultados
        )

        quantidade_atendimentos_total = sum(
            resultado.quantidade_atendimentos
            for resultado in resultados
        )

        km_total = sum(
            resultado.km_total
            for resultado in resultados
        )

        return {
            "caminhoes": resultados,
            "faturamento_total": faturamento_total,
            "quantidade_atendimentos_total":
                quantidade_atendimentos_total,
            "km_total": km_total
        }

    @staticmethod
    def buscar_detalhes(
        id_caminhao,
        data_inicial,
        data_final
    ):

        query = (

            Atendimento.query

            .options(

                joinedload(
                    Atendimento.tabela_valores
                ).joinedload(
                    TabelaValores.administradora
                ),

                joinedload(
                    Atendimento.cliente
                ),

                joinedload(
                    Atendimento.motorista
                ),

                joinedload(
                    Atendimento.caminhao
                )

            )

            .filter(
                Atendimento.fk_caminhao_id_caminhao
                == id_caminhao
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

        return CaminhoesRelatorioService.gerar_relatorio(
            data_inicial,
            data_final
        )