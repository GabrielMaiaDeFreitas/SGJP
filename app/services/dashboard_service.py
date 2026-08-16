from decimal import Decimal

from datetime import date
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from calendar import monthrange

from app import db

from sqlalchemy import func
from sqlalchemy import or_

from app.models import (
    Atendimento,
    Usuario,
    Motorista,
    Caminhao,
    Cliente,
    Administradora,
    TipoServico,
    TabelaValores
)


class DashboardService:

    @staticmethod
    def resumo_periodo(
        data_inicial,
        data_final
    ):

        atendimentos = Atendimento.query.filter(
            Atendimento.data_atendimento >= data_inicial,
            Atendimento.data_atendimento <= data_final
        )

        quantidade_atendimentos = (
            atendimentos.count()
        )

        faturamento_bruto = (
            atendimentos.with_entities(
                func.coalesce(
                    func.sum(
                        Atendimento.valor_total
                    ),
                    0
                )
            ).scalar()
        )

        return {

            "quantidade_atendimentos":
                quantidade_atendimentos,

            "faturamento_bruto":
                Decimal(str(
                    faturamento_bruto
                ))

        }


    @staticmethod
    def resumo_geral():

        quantidade_tabelas_configuradas = (

            db.session.query(
                TabelaValores
                .fk_administradora_id_administradora
            )

            .filter(

                or_(

                    TabelaValores
                    .valor_saida
                    .isnot(None),

                    TabelaValores
                    .valor_km_excedente
                    .isnot(None)

                )

            )

            .distinct()

            .count()

        )

        return {

            "usuarios":
                Usuario.query.filter_by(
                    ativo=True
                ).count(),

            "motoristas":
                Motorista.query.filter_by(
                    ativo=True
                ).count(),

            "caminhoes":
                Caminhao.query.filter_by(
                    ativo=True
                ).count(),

            "clientes":
                Cliente.query.filter_by(
                    ativo=True
                ).count(),

            "administradoras":
                Administradora.query.filter_by(
                    ativo=True
                ).count(),

            "tipos_servico":
                TipoServico.query.filter_by(
                    ativo=True
                ).count(),

            "tabelas_valores":
                quantidade_tabelas_configuradas,

            "atendimentos":
                Atendimento.query.count()

        }


    @staticmethod
    def _subtrair_um_mes(data):

        ano = data.year

        mes = data.month - 1

        if mes == 0:

            mes = 12
            ano -= 1

        ultimo_dia = monthrange(
            ano,
            mes
        )[1]

        dia = min(
            data.day,
            ultimo_dia
        )

        return date(
            ano,
            mes,
            dia
        )


    @staticmethod
    def comparar_periodos(
        data_inicial,
        data_final
    ):

        # Verifica se o período começa no primeiro dia
        # e termina no último dia de um mês.
        periodo_mensal_completo = (
            data_inicial.day == 1
            and (
                data_final + timedelta(days=1)
            ).day == 1
        )

        if periodo_mensal_completo:

            # Quantidade real de meses incluídos no período.
            #
            # Exemplo:
            # 01/06 até 31/07
            #
            # (2026 - 2026) * 12
            # + (7 - 6)
            # + 1
            #
            # = 2 meses
            quantidade_meses = (
                (
                    data_final.year
                    - data_inicial.year
                ) * 12
                + (
                    data_final.month
                    - data_inicial.month
                )
                + 1
            )

            # O período anterior termina exatamente
            # no dia anterior ao início do atual.
            periodo_anterior_final = (
                data_inicial
                - timedelta(days=1)
            )

            # Volta exatamente a quantidade de meses
            # do período atual.
            periodo_anterior_inicial = (
                data_inicial
                - relativedelta(
                    months=quantidade_meses
                )
            )

        else:

            # Para períodos que não representam meses
            # completos, usamos a mesma quantidade de dias.
            duracao = (
                data_final - data_inicial
            ).days + 1

            periodo_anterior_final = (
                data_inicial
                - timedelta(days=1)
            )

            periodo_anterior_inicial = (
                periodo_anterior_final
                - timedelta(days=duracao - 1)
            )

        atual = DashboardService.resumo_periodo(
            data_inicial,
            data_final
        )

        anterior = DashboardService.resumo_periodo(
            periodo_anterior_inicial,
            periodo_anterior_final
        )

        # ==================================================
        # VARIAÇÃO DO FATURAMENTO
        # ==================================================

        faturamento_atual = (
            atual["faturamento_bruto"]
        )

        faturamento_anterior = (
            anterior["faturamento_bruto"]
        )

        if faturamento_anterior == 0:

            percentual_faturamento = None

        else:

            percentual_faturamento = (
                (
                    faturamento_atual
                    - faturamento_anterior
                )
                / faturamento_anterior
            ) * Decimal("100")

        # ==================================================
        # VARIAÇÃO DOS ATENDIMENTOS
        # ==================================================

        quantidade_atual = (
            atual["quantidade_atendimentos"]
        )

        quantidade_anterior = (
            anterior["quantidade_atendimentos"]
        )

        if quantidade_anterior == 0:

            percentual_atendimentos = None

        else:

            percentual_atendimentos = (
                (
                    Decimal(quantidade_atual)
                    - Decimal(quantidade_anterior)
                )
                / Decimal(quantidade_anterior)
            ) * Decimal("100")

        return {

            "atual": atual,

            "anterior": anterior,

            "percentual_faturamento":
                percentual_faturamento,

            "percentual_atendimentos":
                percentual_atendimentos,

            "periodo_anterior_inicial":
                periodo_anterior_inicial,

            "periodo_anterior_final":
                periodo_anterior_final

        }