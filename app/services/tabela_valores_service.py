from decimal import Decimal, InvalidOperation

from app import db

from app.models import (
    Administradora,
    TipoServico,
    TabelaValores
)

from app.filters.tabela_valores import (
    FILTROS_TABELA_VALORES
)

from app.services.filter_service import (
    FilterService
)

from app.exceptions import (
    CampoObrigatorioError,
    ValidacaoError
)


class TabelaValoresService:

    # =====================================================
    # LISTAGEM PRINCIPAL
    # =====================================================

    @staticmethod
    def listar():

        administradoras = (
            Administradora.query
            .order_by(Administradora.nome)
            .all()
        )

        resultado = []

        for administradora in administradoras:

            quantidade_linhas = (
                TabelaValores.query
                .filter_by(
                    fk_administradora_id_administradora=(
                        administradora.id_administradora
                    ),
                    ativo=True
                )
                .count()
            )

            configurada = (
                TabelaValoresService
                ._tabela_configurada(
                    administradora.id_administradora
                )
            )

            resultado.append({

                "administradora":
                    administradora.nome,

                "situacao":
                    (
                        "Configurada"
                        if configurada
                        else "Não Configurada"
                    ),

                "configurada":
                    configurada,

                "quantidade":
                    quantidade_linhas,

                "id_administradora":
                    administradora.id_administradora

            })

        # Não configuradas primeiro.
        # Dentro de cada grupo, ordem alfabética.

        resultado.sort(

            key=lambda item: (

                item["configurada"],

                item["administradora"].lower()

            )

        )

        return resultado


    # =====================================================
    # VERIFICA SE A TABELA ESTÁ CONFIGURADA
    # =====================================================

    @staticmethod
    def _tabela_configurada(
        id_administradora
    ):

        return (
            TabelaValores.query
            .filter(
                TabelaValores
                .fk_administradora_id_administradora
                == id_administradora,

                TabelaValores.ativo.is_(True),

                (
                    TabelaValores.valor_saida.isnot(None)
                    |
                    TabelaValores.valor_km_excedente.isnot(None)
                )
            )
            .first()
            is not None
        )


    @staticmethod
    def tabela_existe(
        id_administradora
    ):

        return TabelaValoresService._tabela_configurada(
            id_administradora
        )


    # =====================================================
    # CARREGAR TABELA
    # =====================================================

    @staticmethod
    def carregar_tabela(
        id_administradora
    ):

        administradora = (
            Administradora.query.get_or_404(
                id_administradora
            )
        )

        tipos_servico = (
            TipoServico.query
            .filter_by(ativo=True)
            .order_by(TipoServico.nome)
            .all()
        )

        tabela = []

        for tipo_servico in tipos_servico:

            registro = (
                TabelaValores.query
                .filter_by(

                    fk_administradora_id_administradora=(
                        id_administradora
                    ),

                    fk_tipo_servico_id_tipo_servico=(
                        tipo_servico.id_tipo_servico
                    ),

                    ativo=True

                )
                .first()
            )

            tabela.append({

                "tipo_servico":
                    tipo_servico,

                "valor_saida":
                    (
                        registro.valor_saida
                        if registro
                        else None
                    ),

                "valor_km_excedente":
                    (
                        registro.valor_km_excedente
                        if registro
                        else None
                    )

            })

        return administradora, tabela


    # =====================================================
    # SALVAR TABELA
    # =====================================================

    @staticmethod
    def salvar_tabela(
        id_administradora,
        dados
    ):

        if not dados:

            raise ValidacaoError(
                "Nenhum dado da tabela de valores foi informado."
            )


        Administradora.query.get_or_404(
            id_administradora
        )


        # -------------------------------------------------
        # Valida tudo ANTES de alterar o banco
        # -------------------------------------------------

        ids_tipos = {

            tipo.id_tipo_servico

            for tipo in (
                TipoServico.query
                .filter_by(ativo=True)
                .all()
            )

        }


        for item in dados:

            id_tipo_servico = (
                item["id_tipo_servico"]
            )

            valor_saida = (
                item["valor_saida"]
            )

            valor_km_excedente = (
                item["valor_km_excedente"]
            )


            if id_tipo_servico not in ids_tipos:

                raise ValidacaoError(
                    "Tipo de serviço inválido."
                )


            TabelaValoresService._validar_valor(
                valor_saida,
                "Valor de saída"
            )

            TabelaValoresService._validar_valor(
                valor_km_excedente,
                "Valor por KM excedente"
            )


        # -------------------------------------------------
        # Atualiza os registros
        # -------------------------------------------------

        for item in dados:

            id_tipo_servico = (
                item["id_tipo_servico"]
            )

            valor_saida = (
                item["valor_saida"]
            )

            valor_km_excedente = (
                item["valor_km_excedente"]
            )


            registro = (
                TabelaValores.query
                .filter_by(

                    fk_administradora_id_administradora=(
                        id_administradora
                    ),

                    fk_tipo_servico_id_tipo_servico=(
                        id_tipo_servico
                    ),

                    ativo=True

                )
                .first()
            )


            # Nada foi informado para esse serviço.
            # Portanto, ele não deve possuir uma
            # configuração ativa.

            if (
                valor_saida is None
                and
                valor_km_excedente is None
            ):

                if registro:

                    registro.ativo = False

                continue


            # Se já existe e não houve alteração,
            # mantém o registro atual.

            if registro:

                if (
                    registro.valor_saida
                    == valor_saida
                    and
                    registro.valor_km_excedente
                    == valor_km_excedente
                ):

                    continue


                # Houve alteração.
                # Mantemos o histórico e criamos
                # uma nova versão.

                registro.ativo = False


            novo = TabelaValores(

                fk_administradora_id_administradora=(
                    id_administradora
                ),

                fk_tipo_servico_id_tipo_servico=(
                    id_tipo_servico
                ),

                valor_saida=(
                    valor_saida
                ),

                valor_km_excedente=(
                    valor_km_excedente
                ),

                ativo=True

            )

            db.session.add(novo)


        db.session.commit()


    # =====================================================
    # VALIDAÇÃO DOS VALORES
    # =====================================================

    @staticmethod
    def _validar_valor(
        valor,
        nome
    ):

        if valor is None:

            return


        try:

            valor = Decimal(str(valor))

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            raise ValidacaoError(
                f"{nome} inválido."
            )


        if valor < 0:

            raise ValidacaoError(
                f"{nome} não pode ser negativo."
            )


    # =====================================================
    # CONVERTE FORMULÁRIO
    # =====================================================

    @staticmethod
    def montar_dados(
        formulario
    ):

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


        if not (
            len(ids)
            == len(valores_saida)
            == len(valores_km)
        ):

            raise ValidacaoError(
                "Os dados da tabela de valores estão inconsistentes."
            )


        for id_tipo, saida, km in zip(

            ids,
            valores_saida,
            valores_km

        ):

            try:

                id_tipo_servico = int(
                    id_tipo
                )

            except (
                ValueError,
                TypeError
            ):

                raise ValidacaoError(
                    "Tipo de serviço inválido."
                )


            valor_saida = (
                TabelaValoresService
                ._converter_decimal(saida)
            )

            valor_km = (
                TabelaValoresService
                ._converter_decimal(km)
            )


            dados.append({

                "id_tipo_servico":
                    id_tipo_servico,

                "valor_saida":
                    valor_saida,

                "valor_km_excedente":
                    valor_km

            })


        return dados


    @staticmethod
    def _converter_decimal(
        valor
    ):

        if valor is None:

            return None


        valor = str(valor).strip()


        if not valor:

            return None


        try:

            return Decimal(valor)

        except InvalidOperation:

            raise ValidacaoError(
                "Um dos valores informados é inválido."
            )


    # =====================================================
    # DETALHES
    # =====================================================

    @staticmethod
    def detalhes(
        id_administradora
    ):

        return TabelaValoresService.carregar_tabela(
            id_administradora
        )


    # =====================================================
    # VISUALIZAÇÃO COMPLETA
    # =====================================================

    @staticmethod
    def listar_completo(
        filtros
    ):

        tabelas = FilterService.listar(

            modelo=TabelaValores,

            filtros=filtros,

            configuracoes=FILTROS_TABELA_VALORES,

            ordenar_por=(
                "fk_administradora_id_administradora"
            )

        )

        tabelas.sort(

            key=lambda tabela: (

                tabela.administradora.nome.lower(),

                tabela.tipo_servico.nome.lower()

            )

        )

        return tabelas


    # =====================================================
    # ADMINISTRADORAS DISPONÍVEIS
    # =====================================================

    @staticmethod
    def administradoras_disponiveis():

        administradoras_configuradas = {

            tabela
            .fk_administradora_id_administradora

            for tabela in (
                TabelaValores.query
                .filter(
                    TabelaValores.ativo.is_(True),

                    (
                        TabelaValores.valor_saida.isnot(None)
                        |
                        TabelaValores.valor_km_excedente.isnot(None)
                    )
                )
                .all()
            )

        }


        return (
            Administradora.query
            .filter(

                Administradora.ativo.is_(True),

                ~Administradora.id_administradora.in_(
                    administradoras_configuradas
                )

            )
            .order_by(
                Administradora.nome
            )
            .all()
        )


    # =====================================================
    # ADMINISTRADORAS CONFIGURADAS
    # =====================================================

    @staticmethod
    def administradoras_configuradas():

        return (
            Administradora.query
            .join(
                TabelaValores,
                TabelaValores
                .fk_administradora_id_administradora
                == Administradora.id_administradora
            )
            .filter(

                Administradora.ativo.is_(True),

                TabelaValores.ativo.is_(True),

                (
                    TabelaValores.valor_saida.isnot(None)
                    |
                    TabelaValores.valor_km_excedente.isnot(None)
                )

            )
            .distinct()
            .order_by(
                Administradora.nome
            )
            .all()
        )


    # =====================================================
    # BUSCAR TABELA
    # =====================================================

    @staticmethod
    def buscar_tabela(
        id_administradora,
        id_tipo_servico
    ):

        return (
            TabelaValores.query
            .filter_by(

                fk_administradora_id_administradora=(
                    id_administradora
                ),

                fk_tipo_servico_id_tipo_servico=(
                    id_tipo_servico
                ),

                ativo=True

            )
            .first()
        )