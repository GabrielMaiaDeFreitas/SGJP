import re

from app import db

from app.models import Caminhao

from app.filters.caminhao import (
    FILTROS_CAMINHAO
)

from app.services.filter_service import (
    FilterService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)


class CaminhaoService:

    @staticmethod
    def listar():

        return Caminhao.query.order_by(

            Caminhao.ativo.desc(),

            Caminhao.modelo

        ).all()


    @staticmethod
    def listar_completo(
        filtros
    ):

        return FilterService.listar(

            modelo=Caminhao,

            filtros=filtros,

            configuracoes=FILTROS_CAMINHAO,

            ordenar_por="modelo"

        )


    @staticmethod
    def buscar_por_id(
        id_caminhao
    ):

        return Caminhao.query.get_or_404(
            id_caminhao
        )


    @staticmethod
    def criar(
        placa,
        modelo
    ):

        dados = CaminhaoService._preparar_dados(
            placa,
            modelo
        )

        CaminhaoService._validar_dados(
            dados
        )

        CaminhaoService._validar_unicidade(
            dados["placa"]
        )


        caminhao = Caminhao(

            placa=dados["placa"],

            modelo=dados["modelo"],

            ativo=True

        )


        db.session.add(
            caminhao
        )

        db.session.commit()

        return caminhao


    @staticmethod
    def atualizar(
        caminhao,
        placa,
        modelo
    ):

        dados = CaminhaoService._preparar_dados(
            placa,
            modelo
        )

        CaminhaoService._validar_dados(
            dados
        )

        CaminhaoService._validar_unicidade(

            dados["placa"],

            id_caminhao=caminhao.id_caminhao

        )


        caminhao.placa = (
            dados["placa"]
        )

        caminhao.modelo = (
            dados["modelo"]
        )


        db.session.commit()

        return caminhao


    @staticmethod
    def alternar_status(
        caminhao
    ):

        caminhao.ativo = not caminhao.ativo

        db.session.commit()

        return caminhao


    # =====================================================
    # PREPARAÇÃO
    # =====================================================

    @staticmethod
    def _preparar_dados(
        placa,
        modelo
    ):

        return {

            "placa":
                CaminhaoService._normalizar_placa(
                    placa
                ),

            "modelo":
                modelo.strip()
                if modelo
                else ""

        }


    # =====================================================
    # NORMALIZAÇÃO DA PLACA
    # =====================================================

    @staticmethod
    def _normalizar_placa(
        placa
    ):

        if not placa:

            return ""


        placa = placa.strip().upper()

        placa = placa.replace(
            " ",
            ""
        )

        placa = placa.replace(
            "-",
            ""
        )


        # Placa antiga:
        #
        # ABC1234
        #
        # passa a ser:
        #
        # ABC-1234

        if re.fullmatch(
            r"[A-Z]{3}[0-9]{4}",
            placa
        ):

            return (
                f"{placa[:3]}-"
                f"{placa[3:]}"
            )


        # Placa Mercosul:
        #
        # ABC1D23
        #
        # permanece:
        #
        # ABC1D23

        if re.fullmatch(
            r"[A-Z]{3}[0-9][A-Z][0-9]{2}",
            placa
        ):

            return placa


        return placa


    # =====================================================
    # VALIDAÇÕES
    # =====================================================

    @staticmethod
    def _validar_dados(
        dados
    ):

        CaminhaoService._validar_obrigatorios(
            dados
        )

        CaminhaoService._validar_modelo(
            dados["modelo"]
        )

        CaminhaoService._validar_placa(
            dados["placa"]
        )


    @staticmethod
    def _validar_obrigatorios(
        dados
    ):

        if not dados["placa"]:

            raise CampoObrigatorioError(
                "placa"
            )


        if not dados["modelo"]:

            raise CampoObrigatorioError(
                "modelo"
            )


    @staticmethod
    def _validar_modelo(
        modelo
    ):

        if len(modelo) > 100:

            raise ValidacaoError(

                "O modelo do caminhão "
                "deve possuir no máximo "
                "100 caracteres."

            )


    @staticmethod
    def _validar_placa(
        placa
    ):

        placa_antiga = re.fullmatch(

            r"[A-Z]{3}-[0-9]{4}",

            placa

        )


        placa_mercosul = re.fullmatch(

            r"[A-Z]{3}[0-9][A-Z][0-9]{2}",

            placa

        )


        if not (
            placa_antiga
            or placa_mercosul
        ):

            raise ValidacaoError(

                "A placa informada não possui "
                "um formato válido. "
                "Use ABC-1234 ou ABC1D23."

            )


    # =====================================================
    # UNICIDADE
    # =====================================================

    @staticmethod
    def _validar_unicidade(
        placa,
        id_caminhao=None
    ):

        query = Caminhao.query.filter(
            Caminhao.placa == placa
        )


        if id_caminhao is not None:

            query = query.filter(

                Caminhao.id_caminhao
                != id_caminhao

            )


        if query.first():

            raise RecursoDuplicadoError(

                "placa",

                placa

            )