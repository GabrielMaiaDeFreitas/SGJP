from app import db

from app.models import Administradora

from app.filters.administradora import (
    FILTROS_ADMINISTRADORA
)

from app.services.filter_service import (
    FilterService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)


class AdministradoraService:

    @staticmethod
    def listar():

        return Administradora.query.order_by(

            Administradora.ativo.desc(),

            Administradora.nome

        ).all()


    @staticmethod
    def listar_completo(
        filtros
    ):

        return FilterService.listar(

            modelo=Administradora,

            filtros=filtros,

            configuracoes=FILTROS_ADMINISTRADORA,

            ordenar_por="nome"

        )


    @staticmethod
    def buscar_por_id(
        id_administradora
    ):

        return Administradora.query.get_or_404(
            id_administradora
        )


    @staticmethod
    def criar(
        nome,
        cliente_proprio
    ):

        nome = AdministradoraService._normalizar_nome(
            nome
        )

        cliente_proprio = (
            AdministradoraService._converter_cliente_proprio(
                cliente_proprio
            )
        )

        AdministradoraService._validar_nome(
            nome
        )

        AdministradoraService._validar_unicidade(
            nome
        )


        administradora = Administradora(

            nome=nome,

            cliente_proprio=cliente_proprio,

            ativo=True

        )


        db.session.add(
            administradora
        )

        db.session.commit()

        return administradora


    @staticmethod
    def atualizar(
        administradora,
        nome,
        cliente_proprio
    ):

        nome = AdministradoraService._normalizar_nome(
            nome
        )

        cliente_proprio = (
            AdministradoraService._converter_cliente_proprio(
                cliente_proprio
            )
        )

        AdministradoraService._validar_nome(
            nome
        )

        AdministradoraService._validar_unicidade(

            nome,

            id_administradora=
                administradora.id_administradora

        )


        if cliente_proprio:

            AdministradoraService._validar_cliente_proprio(
                administradora
            )


        administradora.nome = nome

        administradora.cliente_proprio = (
            cliente_proprio
        )


        db.session.commit()

        return administradora


    @staticmethod
    def alternar_status(
        administradora
    ):

        administradora.ativo = not administradora.ativo

        db.session.commit()

        return administradora


    # =====================================================
    # NORMALIZAÇÃO
    # =====================================================

    @staticmethod
    def _normalizar_nome(
        nome
    ):

        if not nome:

            return ""

        return nome.strip()


    @staticmethod
    def _converter_cliente_proprio(
        valor
    ):

        if isinstance(
            valor,
            bool
        ):

            return valor

        return valor == "Sim"


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

                "O nome da administradora "
                "deve possuir no máximo "
                "100 caracteres."

            )


    @staticmethod
    def _validar_unicidade(
        nome,
        id_administradora=None
    ):

        query = Administradora.query.filter(

            Administradora.nome.ilike(
                nome
            )

        )


        if id_administradora is not None:

            query = query.filter(

                Administradora.id_administradora
                != id_administradora

            )


        if query.first():

            raise RecursoDuplicadoError(

                "nome",

                nome

            )


    @staticmethod
    def _validar_cliente_proprio(
        administradora
    ):

        quantidade_clientes_ativos = sum(

            1

            for cliente in administradora.clientes

            if cliente.ativo

        )


        if quantidade_clientes_ativos > 1:

            raise ValidacaoError(

                (
                    "Não é possível definir esta "
                    "administradora como Cliente Próprio "
                    "porque ela possui mais de um "
                    "cliente ativo cadastrado."
                )

            )

    @staticmethod
    def listar_ativas():

        return (
            Administradora.query
            .filter_by(ativo=True)
            .order_by(Administradora.nome)
            .all()
        )