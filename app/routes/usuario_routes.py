from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

from app.models import Usuario

from app.filters.usuario import FILTROS_USUARIO

from app.services.usuario_service import (
    UsuarioService
)

from app.exceptions import (
    ValidacaoError,
    RecursoDuplicadoError
)

from app.helpers.autorizacao_helper import (
    requer_perfil
)


usuario_bp = Blueprint(
    "usuario",
    __name__,
    url_prefix="/usuarios"
)


@usuario_bp.route("/")
@requer_perfil("Administrador")
def listar():

    usuarios = UsuarioService.listar()

    return render_template(

        "usuarios/listar.html",

        titulo="Gerenciamento de Usuários",

        usuarios=usuarios,

        novo_url=url_for(
            "usuario.novo"
        ),

        novo_texto="Novo Usuário",

        visualizacao_url=url_for(
            "usuario.completo"
        ),

        exportar_url=url_for(
            "exportacao.exportar_generico",
            modulo="usuario"
        )

    )


@usuario_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
@requer_perfil("Administrador")
def novo():

    if request.method == "POST":

        nome = request.form.get(
            "nome"
        )

        login = request.form.get(
            "login"
        )

        perfil = request.form.get(
            "perfil"
        )

        senha = request.form.get(
            "senha"
        )

        confirmar_senha = request.form.get(
            "confirmar_senha"
        )

        try:

            UsuarioService.criar(

                nome=nome,

                login=login,

                perfil=perfil,

                senha=senha,

                confirmar_senha=confirmar_senha

            )

        except ValidacaoError as erro:

            flash(
                erro.mensagem,
                "warning"
            )

            usuario = Usuario(

                nome=nome,

                login=login,

                perfil=perfil

            )

            return render_template(

                "usuarios/form.html",

                titulo="Novo Usuário",

                usuario=usuario,

                editando=False

            )

        except RecursoDuplicadoError as erro:

            flash(
                erro.mensagem,
                "warning"
            )

            usuario = Usuario(

                nome=nome,

                login=login,

                perfil=perfil

            )

            return render_template(

                "usuarios/form.html",

                titulo="Novo Usuário",

                usuario=usuario,

                editando=False

            )


        flash(
            "Usuário cadastrado com sucesso.",
            "success"
        )

        return redirect(
            url_for(
                "usuario.listar"
            )
        )


    return render_template(

        "usuarios/form.html",

        titulo="Novo Usuário",

        usuario=None,

        editando=False

    )


@usuario_bp.route(
    "/<int:id_usuario>/editar",
    methods=["GET", "POST"]
)
@requer_perfil("Administrador")
def editar(id_usuario):

    usuario = UsuarioService.buscar_por_id(
        id_usuario
    )


    if request.method == "POST":

        nome = request.form.get(
            "nome"
        )

        login = request.form.get(
            "login"
        )

        perfil = request.form.get(
            "perfil"
        )

        senha_atual = request.form.get(
            "senha_atual"
        )

        nova_senha = request.form.get(
            "nova_senha"
        )

        confirmar_senha = request.form.get(
            "confirmar_senha"
        )


        try:

            UsuarioService.atualizar(

                usuario=usuario,

                nome=nome,

                login=login,

                perfil=perfil,

                senha_atual=senha_atual,

                nova_senha=nova_senha,

                confirmar_senha=confirmar_senha

            )

        except (
            ValidacaoError,
            RecursoDuplicadoError
        ) as erro:

            flash(
                erro.mensagem,
                "warning"
            )

            usuario.nome = (
                nome or ""
            )

            usuario.login = (
                login or ""
            )

            usuario.perfil = (
                perfil or ""
            )

            return render_template(

                "usuarios/form.html",

                titulo="Editar Usuário",

                usuario=usuario,

                editando=True,

                origem=request.form.get(
                    "origem"
                )

            )


        flash(
            "Usuário atualizado com sucesso.",
            "success"
        )


        origem = request.form.get(
            "origem"
        )


        if origem == "completo":

            return redirect(
                url_for(
                    "usuario.completo"
                )
            )


        return redirect(
            url_for(
                "usuario.listar"
            )
        )


    return render_template(

        "usuarios/form.html",

        titulo="Editar Usuário",

        usuario=usuario,

        editando=True,

        origem=request.args.get(
            "origem"
        )

    )


@usuario_bp.route(
    "/<int:id_usuario>/toggle"
)
@requer_perfil("Administrador")
def toggle(id_usuario):

    usuario = UsuarioService.buscar_por_id(
        id_usuario
    )

    UsuarioService.alternar_status(
        usuario
    )

    flash(
        "Status do usuário atualizado.",
        "success"
    )

    origem = request.args.get(
        "origem"
    )

    if origem == "completo":

        return redirect(
            url_for(
                "usuario.completo"
            )
        )

    return redirect(
        url_for(
            "usuario.listar"
        )
    )


@usuario_bp.route(
    "/<int:id_usuario>"
)
@requer_perfil("Administrador")
def detalhes(id_usuario):

    usuario = UsuarioService.buscar_por_id(
        id_usuario
    )

    return render_template(

        "usuarios/detalhes.html",

        titulo="Detalhes do Usuário",

        usuario=usuario

    )


@usuario_bp.route(
    "/completo"
)
@requer_perfil("Administrador")
def completo():

    usuarios = UsuarioService.listar_completo(
        request.args
    )

    return render_template(

        "usuarios/completo.html",

        titulo="Visualização Completa de Usuários",

        usuarios=usuarios,

        campos=FILTROS_USUARIO,

        campos_filtro=request.args.getlist(
            "campo[]"
        ),

        valores_filtro=request.args.getlist(
            "valor[]"
        )

    )


@usuario_bp.route(
    "/meu-perfil",
    methods=["GET", "POST"]
)
@requer_perfil(
    "Administrador",
    "Operador",
    "Leitor"
)
def meu_perfil():

    usuario = UsuarioService.buscar_por_id(
        session["usuario_id"]
    )


    if request.method == "POST":

        if session.get("perfil") == "Administrador":

            nome = request.form.get(
                "nome"
            )

            login = request.form.get(
                "login"
            )

            perfil = request.form.get(
                "perfil"
            )

        else:

            nome = usuario.nome

            login = usuario.login

            perfil = usuario.perfil


        senha_atual = request.form.get(
            "senha_atual"
        )

        nova_senha = request.form.get(
            "nova_senha"
        )

        confirmar_senha = request.form.get(
            "confirmar_senha"
        )


        try:

            UsuarioService.atualizar(

                usuario=usuario,

                nome=nome,

                login=login,

                perfil=perfil,

                senha_atual=senha_atual,

                nova_senha=nova_senha,

                confirmar_senha=confirmar_senha

            )

        except (
            ValidacaoError,
            RecursoDuplicadoError
        ) as erro:

            flash(
                erro.mensagem,
                "warning"
            )

            usuario.nome = (
                nome or ""
            )

            usuario.login = (
                login or ""
            )

            usuario.perfil = (
                perfil or ""
            )

            return render_template(

                "usuarios/meu_perfil.html",

                titulo="Meu Perfil",

                usuario=usuario

            )


        session["usuario_nome"] = (
            usuario.nome
        )

        session["perfil"] = (
            usuario.perfil
        )


        flash(
            "Perfil atualizado com sucesso.",
            "success"
        )

        return redirect(
            url_for(
                "usuario.meu_perfil"
            )
        )


    return render_template(

        "usuarios/meu_perfil.html",

        titulo="Meu Perfil",

        usuario=usuario

    )