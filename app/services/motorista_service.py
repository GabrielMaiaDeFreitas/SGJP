import re

from datetime import datetime

from app import db

from app.models import Motorista

from app.constants.motorista import (
    CATEGORIAS_CNH
)

from app.filters.motorista import (
    FILTROS_MOTORISTA
)

from app.services.filter_service import (
    FilterService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)


class MotoristaService:

    @staticmethod
    def listar():

        return Motorista.query.order_by(

            Motorista.ativo.desc(),

            Motorista.nome

        ).all()


    @staticmethod
    def listar_completo(
        filtros
    ):

        return FilterService.listar(

            modelo=Motorista,

            filtros=filtros,

            configuracoes=FILTROS_MOTORISTA,

            ordenar_por="nome"

        )


    @staticmethod
    def buscar_por_id(
        id_motorista
    ):

        return Motorista.query.get_or_404(
            id_motorista
        )


    @staticmethod
    def criar(
        matricula,
        nome,
        numero_cnh,
        categoria_cnh,
        validade_cnh,
        validade_toxicologico
    ):

        dados = MotoristaService._preparar_dados(

            matricula,

            nome,

            numero_cnh,

            categoria_cnh,

            validade_cnh,

            validade_toxicologico

        )

        MotoristaService._validar_dados(
            dados
        )

        MotoristaService._validar_unicidade(
            dados["matricula"],
            dados["numero_cnh"]
        )


        motorista = Motorista(

            matricula=dados["matricula"],

            nome=dados["nome"],

            numero_cnh=dados["numero_cnh"],

            categoria_cnh=dados["categoria_cnh"],

            validade_cnh=dados["validade_cnh"],

            validade_toxicologico=
                dados["validade_toxicologico"],

            ativo=True

        )


        db.session.add(
            motorista
        )

        db.session.commit()

        return motorista


    @staticmethod
    def atualizar(
        motorista,
        matricula,
        nome,
        numero_cnh,
        categoria_cnh,
        validade_cnh,
        validade_toxicologico
    ):

        dados = MotoristaService._preparar_dados(

            matricula,

            nome,

            numero_cnh,

            categoria_cnh,

            validade_cnh,

            validade_toxicologico

        )

        MotoristaService._validar_dados(
            dados
        )

        MotoristaService._validar_unicidade(

            dados["matricula"],

            dados["numero_cnh"],

            id_motorista=motorista.id_motorista

        )


        motorista.matricula = (
            dados["matricula"]
        )

        motorista.nome = (
            dados["nome"]
        )

        motorista.numero_cnh = (
            dados["numero_cnh"]
        )

        motorista.categoria_cnh = (
            dados["categoria_cnh"]
        )

        motorista.validade_cnh = (
            dados["validade_cnh"]
        )

        motorista.validade_toxicologico = (
            dados["validade_toxicologico"]
        )


        db.session.commit()

        return motorista


    @staticmethod
    def alternar_status(
        motorista
    ):

        motorista.ativo = not motorista.ativo

        db.session.commit()

        return motorista


    # =====================================================
    # PREPARAÇÃO
    # =====================================================

    @staticmethod
    def _preparar_dados(
        matricula,
        nome,
        numero_cnh,
        categoria_cnh,
        validade_cnh,
        validade_toxicologico
    ):

        return {

            "matricula":
                matricula.strip()
                if matricula
                else "",

            "nome":
                nome.strip()
                if nome
                else "",

            "numero_cnh":
                numero_cnh.strip()
                if numero_cnh
                else "",

            "categoria_cnh":
                categoria_cnh.strip()
                if categoria_cnh
                else "",

            "validade_cnh":
                MotoristaService._converter_data(
                    validade_cnh,
                    "validade da CNH"
                ),

            "validade_toxicologico":
                MotoristaService._converter_data(
                    validade_toxicologico,
                    "validade do toxicológico"
                )

        }


    # =====================================================
    # VALIDAÇÕES
    # =====================================================

    @staticmethod
    def _validar_dados(
        dados
    ):

        MotoristaService._validar_obrigatorios(
            dados
        )

        MotoristaService._validar_tamanhos(
            dados
        )

        MotoristaService._validar_cnh(
            dados["numero_cnh"]
        )

        MotoristaService._validar_categoria(
            dados["categoria_cnh"]
        )


    @staticmethod
    def _validar_obrigatorios(
        dados
    ):

        campos = {

            "matrícula":
                dados["matricula"],

            "nome":
                dados["nome"],

            "número da CNH":
                dados["numero_cnh"],

            "categoria da CNH":
                dados["categoria_cnh"],

            "validade da CNH":
                dados["validade_cnh"],

            "validade do toxicológico":
                dados["validade_toxicologico"]

        }


        for campo, valor in campos.items():

            if not valor:

                raise CampoObrigatorioError(
                    campo
                )


    @staticmethod
    def _validar_tamanhos(
        dados
    ):

        limites = {

            "matrícula": (
                dados["matricula"],
                20
            ),

            "nome": (
                dados["nome"],
                100
            ),

            "número da CNH": (
                dados["numero_cnh"],
                20
            ),

            "categoria da CNH": (
                dados["categoria_cnh"],
                5
            )

        }


        for campo, (
            valor,
            limite
        ) in limites.items():

            if len(valor) > limite:

                raise ValidacaoError(

                    f"O campo {campo} "
                    f"deve possuir no máximo "
                    f"{limite} caracteres."

                )


    @staticmethod
    def _validar_cnh(
        numero_cnh
    ):

        if not re.fullmatch(
            r"[0-9]{11}",
            numero_cnh
        ):

            raise ValidacaoError(

                "O número da CNH deve possuir "
                "exatamente 11 dígitos numéricos."

            )


    @staticmethod
    def _validar_categoria(
        categoria_cnh
    ):

        if categoria_cnh not in CATEGORIAS_CNH:

            raise ValidacaoError(

                "Categoria de CNH inválida."

            )


    # =====================================================
    # DATAS
    # =====================================================

    @staticmethod
    def _converter_data(
        valor,
        nome_campo
    ):

        if not valor:

            return None


        try:

            return datetime.strptime(
                valor,
                "%Y-%m-%d"
            ).date()

        except (
            ValueError,
            TypeError
        ):

            raise ValidacaoError(

                f"A {nome_campo} "
                "deve ser uma data válida."

            )


    # =====================================================
    # UNICIDADE
    # =====================================================

    @staticmethod
    def _validar_unicidade(
        matricula,
        numero_cnh,
        id_motorista=None
    ):

        query_matricula = Motorista.query.filter(
            Motorista.matricula == matricula
        )


        query_cnh = Motorista.query.filter(
            Motorista.numero_cnh == numero_cnh
        )


        if id_motorista is not None:

            query_matricula = query_matricula.filter(

                Motorista.id_motorista
                != id_motorista

            )

            query_cnh = query_cnh.filter(

                Motorista.id_motorista
                != id_motorista

            )


        if query_matricula.first():

            raise RecursoDuplicadoError(

                "matrícula",

                matricula

            )


        if query_cnh.first():

            raise RecursoDuplicadoError(

                "número da CNH",

                numero_cnh

            )