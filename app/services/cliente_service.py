from app import db

from app.models import (
    Cliente,
    Administradora
)

from app.filters.cliente import (
    FILTROS_CLIENTE
)

from app.services.filter_service import (
    FilterService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)


class ClienteService:

    @staticmethod
    def listar():

        return Cliente.query.order_by(

            Cliente.ativo.desc(),

            Cliente.nome_fantasia

        ).all()


    @staticmethod
    def listar_completo(
        filtros
    ):

        return FilterService.listar(

            modelo=Cliente,

            filtros=filtros,

            configuracoes=FILTROS_CLIENTE,

            ordenar_por="nome_fantasia"

        )


    @staticmethod
    def buscar_por_id(
        id_cliente
    ):

        return Cliente.query.get_or_404(
            id_cliente
        )


    @staticmethod
    def listar_por_administradora(
        id_administradora
    ):

        administradora = (
            Administradora.query.get_or_404(
                id_administradora
            )
        )

        clientes = Cliente.query.filter_by(

            ativo=True,

            fk_administradora_id_administradora=
                id_administradora

        ).order_by(

            Cliente.nome_fantasia

        ).all()

        return {

            "cliente_proprio":
                administradora.cliente_proprio,

            "clientes": [

                {
                    "id": cliente.id_cliente,
                    "nome": cliente.nome_fantasia
                }

                for cliente in clientes

            ]

        }


    @staticmethod
    def criar(
        nome_fantasia,
        razao_social,
        cnpj,
        id_administradora,
        origem=None
    ):

        nome_fantasia = (
            ClienteService._normalizar_texto(
                nome_fantasia
            )
        )

        razao_social = (
            ClienteService._normalizar_texto(
                razao_social
            )
        )

        cnpj = (
            ClienteService._normalizar_cnpj(
                cnpj
            )
        )


        ClienteService._validar_nome_fantasia(
            nome_fantasia
        )

        ClienteService._validar_razao_social(
            razao_social
        )

        ClienteService._validar_cnpj(
            cnpj
        )


        administradora = (
            ClienteService._buscar_administradora(
                id_administradora
            )
        )


        ClienteService._validar_administradora(

            administradora,

            origem

        )


        ClienteService._validar_cnpj_unico(
            cnpj
        )


        cliente = Cliente(

            nome_fantasia=nome_fantasia,

            razao_social=razao_social,

            cnpj=cnpj,

            ativo=True,

            fk_administradora_id_administradora=(
                administradora.id_administradora
            )

        )


        db.session.add(cliente)

        db.session.commit()

        return cliente


    @staticmethod
    def atualizar(
        cliente,
        nome_fantasia,
        razao_social,
        cnpj,
        id_administradora
    ):

        nome_fantasia = (
            ClienteService._normalizar_texto(
                nome_fantasia
            )
        )

        razao_social = (
            ClienteService._normalizar_texto(
                razao_social
            )
        )

        cnpj = (
            ClienteService._normalizar_cnpj(
                cnpj
            )
        )


        ClienteService._validar_nome_fantasia(
            nome_fantasia
        )

        ClienteService._validar_razao_social(
            razao_social
        )

        ClienteService._validar_cnpj(
            cnpj
        )


        administradora = (
            ClienteService._buscar_administradora(
                id_administradora
            )
        )


        ClienteService._validar_administradora(
            administradora
        )


        ClienteService._validar_cnpj_unico(

            cnpj,

            id_cliente=cliente.id_cliente

        )


        cliente.nome_fantasia = (
            nome_fantasia
        )

        cliente.razao_social = (
            razao_social
        )

        cliente.cnpj = cnpj

        cliente.fk_administradora_id_administradora = (
            administradora.id_administradora
        )


        db.session.commit()

        return cliente


    @staticmethod
    def alternar_status(
        cliente
    ):

        cliente.ativo = not cliente.ativo

        db.session.commit()

        return cliente


    @staticmethod
    def cancelar_cadastro_proprio(
        id_administradora
    ):

        administradora = (
            Administradora.query.get_or_404(
                id_administradora
            )
        )

        db.session.delete(
            administradora
        )

        db.session.commit()


    # =====================================================
    # NORMALIZAÇÃO
    # =====================================================

    @staticmethod
    def _normalizar_texto(
        valor
    ):

        if not valor:

            return ""

        return " ".join(
            valor.strip().split()
        )


    @staticmethod
    def _normalizar_cnpj(
        cnpj
    ):

        if not cnpj:

            return ""

        return "".join(

            caractere

            for caractere in cnpj

            if caractere.isdigit()

        )


    # =====================================================
    # BUSCA
    # =====================================================

    @staticmethod
    def _buscar_administradora(
        id_administradora
    ):

        if not id_administradora:

            raise CampoObrigatorioError(
                "administradora"
            )


        administradora = (
            Administradora.query.get(
                id_administradora
            )
        )


        if not administradora:

            raise ValidacaoError(
                "A administradora selecionada não existe."
            )


        return administradora


    # =====================================================
    # VALIDAÇÕES
    # =====================================================

    @staticmethod
    def _validar_nome_fantasia(
        nome
    ):

        if not nome:

            raise CampoObrigatorioError(
                "nome fantasia"
            )


        if len(nome) > 100:

            raise ValidacaoError(

                "O nome fantasia deve possuir "
                "no máximo 100 caracteres."

            )


    @staticmethod
    def _validar_razao_social(
        razao_social
    ):

        if not razao_social:

            raise CampoObrigatorioError(
                "razão social"
            )


        if len(razao_social) > 150:

            raise ValidacaoError(

                "A razão social deve possuir "
                "no máximo 150 caracteres."

            )


    @staticmethod
    def _validar_cnpj(
        cnpj
    ):

        if not cnpj:

            raise CampoObrigatorioError(
                "CNPJ"
            )


        if len(cnpj) != 14:

            raise ValidacaoError(

                "O CNPJ deve possuir 14 dígitos."

            )


        if not cnpj.isdigit():

            raise ValidacaoError(

                "O CNPJ deve conter somente números."

            )


        if len(set(cnpj)) == 1:

            raise ValidacaoError(
                "O CNPJ informado é inválido."
            )


        if not ClienteService._validar_digitos_cnpj(
            cnpj
        ):

            raise ValidacaoError(
                "O CNPJ informado é inválido."
            )


    @staticmethod
    def _validar_digitos_cnpj(
        cnpj
    ):

        numeros = [
            int(numero)
            for numero in cnpj
        ]


        pesos_primeiro = (
            5, 4, 3, 2,
            9, 8, 7, 6, 5, 4, 3, 2
        )

        soma = sum(

            numero * peso

            for numero, peso
            in zip(
                numeros[:12],
                pesos_primeiro
            )

        )

        resto = soma % 11

        digito_1 = (
            0
            if resto < 2
            else 11 - resto
        )


        pesos_segundo = (
            6, 5, 4, 3, 2,
            9, 8, 7, 6, 5, 4, 3, 2
        )

        soma = sum(

            numero * peso

            for numero, peso
            in zip(
                numeros[:12] + [digito_1],
                pesos_segundo
            )

        )

        resto = soma % 11

        digito_2 = (
            0
            if resto < 2
            else 11 - resto
        )


        return (
            numeros[12] == digito_1
            and numeros[13] == digito_2
        )


    @staticmethod
    def _validar_cnpj_unico(
        cnpj,
        id_cliente=None
    ):

        query = Cliente.query.filter(
            Cliente.cnpj == cnpj
        )


        if id_cliente is not None:

            query = query.filter(

                Cliente.id_cliente
                != id_cliente

            )


        if query.first():

            raise RecursoDuplicadoError(
                "CNPJ",
                cnpj
            )


    @staticmethod
    def _validar_administradora(
        administradora,
        origem=None
    ):

        if not administradora.ativo:

            raise ValidacaoError(

                "A administradora selecionada "
                "está inativa."

            )


        if (
            administradora.cliente_proprio
            and origem != "administradora"
        ):

            raise ValidacaoError(

                (
                    "Esta administradora está marcada "
                    "como Cliente Próprio. O cliente "
                    "deve ser cadastrado pelo fluxo "
                    "da própria administradora."
                )

            )