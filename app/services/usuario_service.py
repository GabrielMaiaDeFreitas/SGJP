from app import db

from app.models import Usuario

from app.filters.usuario import FILTROS_USUARIO

from app.services.filter_service import FilterService

from app.exceptions import (
    CampoObrigatorioError,
    SenhaInvalidaError,
    RecursoDuplicadoError,
    ValidacaoError
)


class UsuarioService:

    PERFIS_VALIDOS = [
        "Administrador",
        "Operador",
        "Leitor"
    ]

    @staticmethod
    def listar():

        return Usuario.query.order_by(
            Usuario.ativo.desc(),
            Usuario.nome
        ).all()

    @staticmethod
    def listar_completo(filtros):

        return FilterService.listar(

            modelo=Usuario,

            filtros=filtros,

            configuracoes=FILTROS_USUARIO,

            ordenar_por="nome"

        )


    @staticmethod
    def buscar_por_id(
        id_usuario
    ):

        return Usuario.query.get_or_404(
            id_usuario
        )


    @staticmethod
    def criar(
        nome,
        login,
        perfil,
        senha,
        confirmar_senha
    ):

        nome = (
            nome.strip()
            if nome
            else ""
        )

        login = (
            login.strip()
            if login
            else ""
        )

        perfil = (
            perfil.strip()
            if perfil
            else ""
        )

        senha = (
            senha.strip()
            if senha
            else ""
        )

        confirmar_senha = (
            confirmar_senha.strip()
            if confirmar_senha
            else ""
        )


        UsuarioService._validar_dados_basicos(
            nome,
            login,
            perfil
        )


        if not senha:

            raise CampoObrigatorioError(
                "senha"
            )


        if senha != confirmar_senha:

            raise ValidacaoError(
                "A confirmação da senha não confere.",
                campo="confirmar_senha"
            )


        UsuarioService._validar_senha(
            senha
        )


        UsuarioService._validar_login_unico(
            login
        )


        usuario = Usuario(

            nome=nome,

            login=login,

            perfil=perfil,

            ativo=True

        )

        usuario.set_senha(
            senha
        )

        db.session.add(
            usuario
        )

        db.session.commit()

        return usuario


    @staticmethod
    def atualizar(
        usuario,
        nome,
        login,
        perfil,
        senha_atual="",
        nova_senha="",
        confirmar_senha=""
    ):

        nome = (
            nome.strip()
            if nome
            else ""
        )

        login = (
            login.strip()
            if login
            else ""
        )

        perfil = (
            perfil.strip()
            if perfil
            else ""
        )

        senha_atual = (
            senha_atual.strip()
            if senha_atual
            else ""
        )

        nova_senha = (
            nova_senha.strip()
            if nova_senha
            else ""
        )

        confirmar_senha = (
            confirmar_senha.strip()
            if confirmar_senha
            else ""
        )


        UsuarioService._validar_dados_basicos(
            nome,
            login,
            perfil
        )


        UsuarioService._validar_login_unico(
            login,
            id_usuario=usuario.id_usuario
        )


        usuario.nome = nome

        usuario.login = login

        usuario.perfil = perfil


        if (
            senha_atual
            or nova_senha
            or confirmar_senha
        ):

            UsuarioService._alterar_senha(
                usuario,
                senha_atual,
                nova_senha,
                confirmar_senha
            )


        db.session.commit()

        return usuario


    @staticmethod
    def alterar_senha(
        usuario,
        senha_atual,
        nova_senha,
        confirmar_senha
    ):

        UsuarioService._alterar_senha(
            usuario,
            senha_atual,
            nova_senha,
            confirmar_senha
        )

        db.session.commit()


    @staticmethod
    def alternar_status(
        usuario
    ):

        usuario.ativo = not usuario.ativo

        db.session.commit()

        return usuario


    @staticmethod
    def _validar_dados_basicos(
        nome,
        login,
        perfil
    ):

        if not nome:

            raise CampoObrigatorioError(
                "nome"
            )


        if not login:

            raise CampoObrigatorioError(
                "login"
            )


        if not perfil:

            raise CampoObrigatorioError(
                "perfil"
            )


        UsuarioService._validar_perfil(
            perfil
        )


    @staticmethod
    def _validar_perfil(
        perfil
    ):

        if perfil not in UsuarioService.PERFIS_VALIDOS:

            raise ValidacaoError(
                "Perfil inválido.",
                campo="perfil"
            )


    @staticmethod
    def _validar_login_unico(
        login,
        id_usuario=None
    ):

        query = Usuario.query.filter(
            Usuario.login.ilike(login)
        )

        if id_usuario is not None:

            query = query.filter(
                Usuario.id_usuario != id_usuario
            )


        usuario_existente = query.first()


        if usuario_existente:

            raise RecursoDuplicadoError(
                "login",
                login
            )


    @staticmethod
    def _validar_senha(
        senha
    ):

        if len(senha) < 8:

            raise SenhaInvalidaError(
                "A senha deve possuir pelo menos 8 caracteres."
            )


    @staticmethod
    def _alterar_senha(
        usuario,
        senha_atual,
        nova_senha,
        confirmar_senha
    ):

        if not senha_atual:

            raise CampoObrigatorioError(
                "senha atual"
            )


        if not usuario.verificar_senha(
            senha_atual
        ):

            raise SenhaInvalidaError(
                "Senha atual incorreta."
            )


        if not nova_senha:

            raise CampoObrigatorioError(
                "nova senha"
            )


        if nova_senha != confirmar_senha:

            raise ValidacaoError(
                "A confirmação da nova senha não confere.",
                campo="confirmar_senha"
            )


        if senha_atual == nova_senha:

            raise SenhaInvalidaError(
                "A nova senha deve ser diferente da senha atual."
            )


        UsuarioService._validar_senha(
            nova_senha
        )


        usuario.set_senha(
            nova_senha
        )