from decimal import Decimal

from app import db

from app.models import (
    Administradora,
    TipoServico,
    TabelaValores
)

from app.filters.tabela_valores import FILTROS_TABELA_VALORES
from app.services.filter_service import FilterService


class TabelaValoresService:

    @staticmethod
    def listar(filtros):

        administradoras = Administradora.query.order_by(

            Administradora.nome

        ).all()

        resultado = []

        for administradora in administradoras:

            quantidade = TabelaValores.query.filter_by(

                fk_administradora_id_administradora=(
                    administradora.id_administradora
                ),

                ativo=True

            ).count()

            configurada = quantidade > 0

            resultado.append({

                "administradora": administradora.nome,

                "situacao": (

                    "Configurada"

                    if configurada

                    else "Não Configurada"

                ),

                "configurada": configurada,

                "quantidade": quantidade,

                "id_administradora": administradora.id_administradora

            })

        resultado.sort(

            key=lambda item: (

                item["configurada"],

                item["administradora"].lower()

            )

        )

        return resultado

    @staticmethod
    def carregar_tabela(id_administradora):

        administradora = Administradora.query.get_or_404(

            id_administradora

        )

        tipos_servico = TipoServico.query.filter_by(

            ativo=True

        ).order_by(

            TipoServico.nome

        ).all()

        tabela = []

        for tipo_servico in tipos_servico:

            registro = TabelaValores.query.filter_by(

                fk_administradora_id_administradora=(
                    id_administradora
                ),

                fk_tipo_servico_id_tipo_servico=(
                    tipo_servico.id_tipo_servico
                ),

                ativo=True

            ).first()

            tabela.append({

                "tipo_servico": tipo_servico,

                "valor_saida": (

                    registro.valor_saida

                    if registro

                    else Decimal("0.00")

                ),

                "valor_km_excedente": (

                    registro.valor_km_excedente

                    if registro

                    else Decimal("0.00")

                )

            })

        return administradora, tabela

    @staticmethod
    def _servico_prestado(

        valor_saida,

        valor_km_excedente

    ):

        return (

            valor_saida > 0

            or

            valor_km_excedente > 0

        )

    @staticmethod
    def salvar_tabela(

        id_administradora,

        dados

    ):

        for item in dados:

            tipo_servico = item["id_tipo_servico"]

            valor_saida = item["valor_saida"]

            valor_km = item["valor_km_excedente"]

            registro = TabelaValores.query.filter_by(

                fk_administradora_id_administradora=(
                    id_administradora
                ),

                fk_tipo_servico_id_tipo_servico=(
                    tipo_servico
                ),

                ativo=True

            ).first()

            if registro:

                if (

                    registro.valor_saida == valor_saida

                    and

                    registro.valor_km_excedente == valor_km

                ):

                    continue

                registro.ativo = False

            if not TabelaValoresService._servico_prestado(

                valor_saida,

                valor_km

            ):

                continue

            novo = TabelaValores(

                fk_administradora_id_administradora=(
                    id_administradora
                ),

                fk_tipo_servico_id_tipo_servico=(
                    tipo_servico
                ),

                valor_saida=valor_saida,

                valor_km_excedente=valor_km,

                ativo=True

            )

            db.session.add(novo)

        db.session.commit()

    @staticmethod
    def montar_dados(formulario):

        dados = []

        ids = formulario.getlist(
            "id_tipo_servico[]"
        )

        valores_saida = formulario.getlist(
            "valor_saida[]"
        )

        valores_km = formulario.getlist(
            "valor_km_excedente[]"
        )

        for id_tipo, saida, km in zip(

            ids,

            valores_saida,

            valores_km

        ):

            dados.append({

                "id_tipo_servico": int(id_tipo),

                "valor_saida": Decimal(
                    saida or "0"
                ),

                "valor_km_excedente": Decimal(
                    km or "0"
                )

            })

        return dados

    @staticmethod
    def detalhes(id_administradora):

        return TabelaValoresService.carregar_tabela(
            id_administradora
        )

    @staticmethod
    def listar_completo(filtros):

        tabelas = FilterService.listar(

            modelo=TabelaValores,

            filtros=filtros,

            configuracoes=FILTROS_TABELA_VALORES,

            ordenar_por="fk_administradora_id_administradora"

        )

        tabelas.sort(

            key=lambda tabela: (

                tabela.administradora.nome.lower(),

                tabela.tipo_servico.nome.lower()

            )

        )

        return tabelas

    @staticmethod
    def administradoras_disponiveis():

        ids_configurados = {

            tabela.fk_administradora_id_administradora

            for tabela in TabelaValores.query.filter_by(

                ativo=True

            ).all()

        }

        return Administradora.query.filter(

            Administradora.ativo.is_(True),

            ~Administradora.id_administradora.in_(

                ids_configurados

            )

        ).order_by(

            Administradora.nome

        ).all()

    @staticmethod
    def tabela_existe(id_administradora):

        return TabelaValores.query.filter_by(

            fk_administradora_id_administradora=id_administradora,

            ativo=True

        ).first() is not None