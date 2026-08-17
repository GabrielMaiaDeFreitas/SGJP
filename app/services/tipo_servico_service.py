from app import db

from app.models import TipoServico

from app.filters.tipo_servico import (
    FILTROS_TIPO_SERVICO
)

from app.services.filter_service import (
    FilterService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)


class TipoServicoService:

    @staticmethod
    def listar():

        return TipoServico.query.order_by(

            TipoServico.ativo.desc(),

            TipoServico.nome

        ).all()


    @staticmethod
    def listar_completo(
        filtros
    ):

        return FilterService.listar(

            modelo=TipoServico,

            filtros=filtros,

            configuracoes=FILTROS_TIPO_SERVICO,

            ordenar_por="nome"

        )


    @staticmethod
    def buscar_por_id(
        id_tipo_servico
    ):

        return TipoServico.query.get_or_404(
            id_tipo_servico
        )


    @staticmethod
    def criar(
        nome
    ):

        nome = (
            TipoServicoService._normalizar_nome(
                nome
            )
        )

        TipoServicoService._validar_nome(
            nome
        )

        TipoServicoService._validar_unicidade(
            nome
        )

        tipo_servico = TipoServico(

            nome=nome,

            ativo=True

        )

        db.session.add(
            tipo_servico
        )

        db.session.commit()

        return tipo_servico


    @staticmethod
    def atualizar(
        tipo_servico,
        nome
    ):

        nome = (
            TipoServicoService._normalizar_nome(
                nome
            )
        )

        TipoServicoService._validar_nome(
            nome
        )

        TipoServicoService._validar_unicidade(

            nome,

            id_tipo_servico=
                tipo_servico.id_tipo_servico

        )

        tipo_servico.nome = nome

        db.session.commit()

        return tipo_servico


    @staticmethod
    def alternar_status(
        tipo_servico
    ):

        tipo_servico.ativo = not tipo_servico.ativo

        db.session.commit()

        return tipo_servico


    # =====================================================
    # NORMALIZAÇÃO
    # =====================================================

    @staticmethod
    def _normalizar_nome(
        nome
    ):

        if not nome:

            return ""

        return " ".join(
            nome.strip().split()
        )


    # =====================================================
    # VALIDAÇÕES
    # =====================================================

    @staticmethod
    def _validar_nome(
        nome
    ):

        if not nome:

            raise CampoObrigatorioError(
                "nome"
            )


        if len(nome) > 100:

            raise ValidacaoError(

                "O nome do tipo de serviço "
                "deve possuir no máximo "
                "100 caracteres."

            )


    @staticmethod
    def _validar_unicidade(
        nome,
        id_tipo_servico=None
    ):

        query = TipoServico.query.filter(

            TipoServico.nome.ilike(
                nome
            )

        )


        if id_tipo_servico is not None:

            query = query.filter(

                TipoServico.id_tipo_servico
                != id_tipo_servico

            )


        if query.first():

            raise RecursoDuplicadoError(

                "nome",

                nome

            )

    @staticmethod
    def listar_ativos():

        return (
            TipoServico.query
            .filter_by(ativo=True)
            .order_by(TipoServico.nome)
            .all()
        )