from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

from app import db
from app.models import Usuario
from app.filters.usuario import FILTROS_USUARIO
from app.services.usuario_service import UsuarioService
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

    usuarios = Usuario.query.order_by(
        Usuario.nome
    ).all()

    return render_template(

        "usuarios/listar.html",

        titulo="Gerenciamento de Usuários",

        usuarios=usuarios,

        novo_url=url_for("usuario.novo"),

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

        def voltar_formulario():

            usuario = Usuario(

                nome=request.form["nome"],

                login=request.form["login"],

                perfil=request.form["perfil"]

            )

            return render_template(

                "usuarios/form.html",

                titulo="Novo Usuário",

                usuario=usuario,

                editando=False

            )

        senha = request.form["senha"].strip()

        confirmar_senha = (
            request.form["confirmar_senha"].strip()
        )

        if not senha:

            flash(
                "Informe uma senha.",
                "warning"
            )

            return voltar_formulario()

        if senha != confirmar_senha:

            flash(
                "A confirmação da senha não confere.",
                "warning"
            )

            return voltar_formulario()

        if Usuario.query.filter(
            Usuario.login.ilike(
                request.form["login"]
            )
        ).first():

            flash(
                "Já existe um usuário com esse login.",
                "warning"
            )

            return voltar_formulario()

        usuario = Usuario(

            nome=request.form["nome"],

            login=request.form["login"],

            perfil=request.form["perfil"],

            ativo=True

        )

        usuario.set_senha(senha)

        db.session.add(usuario)

        db.session.commit()

        flash(
            "Usuário cadastrado com sucesso.",
            "success"
        )

        return redirect(
            url_for("usuario.listar")
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

    usuario = Usuario.query.get_or_404(
        id_usuario
    )

    if request.method == "POST":

        def voltar_formulario():

            usuario.nome = request.form["nome"]

            usuario.login = request.form["login"]

            usuario.perfil = request.form["perfil"]

            return render_template(

                "usuarios/form.html",

                titulo="Editar Usuário",

                usuario=usuario,

                editando=True

            )

        usuario_existente = Usuario.query.filter(

            Usuario.login.ilike(
                request.form["login"]
            ),

            Usuario.id_usuario != id_usuario

        ).first()

        if usuario_existente:

            flash(
                "Já existe um usuário com esse login.",
                "warning"
            )

            return voltar_formulario()

        usuario.nome = request.form["nome"]

        usuario.login = request.form["login"]

        usuario.perfil = request.form["perfil"]

        senha_atual = (
            request.form["senha_atual"].strip()
        )

        nova_senha = (
            request.form["nova_senha"].strip()
        )

        confirmar_senha = (
            request.form["confirmar_senha"].strip()
        )

        if (
            senha_atual
            or nova_senha
            or confirmar_senha
        ):

            if not senha_atual:

                flash(
                    "Informe a senha atual.",
                    "warning"
                )

                return voltar_formulario()

            if not usuario.verificar_senha(
                senha_atual
            ):

                flash(
                    "Senha atual incorreta.",
                    "error"
                )

                return voltar_formulario()

            if not nova_senha:

                flash(
                    "Informe a nova senha.",
                    "warning"
                )

                return voltar_formulario()

            if nova_senha != confirmar_senha:

                flash(
                    "A confirmação da nova senha não confere.",
                    "warning"
                )

                return voltar_formulario()

            if senha_atual == nova_senha:

                flash(
                    "A nova senha deve ser diferente da senha atual.",
                    "warning"
                )

                return voltar_formulario()

            usuario.set_senha(
                nova_senha
            )

        db.session.commit()

        flash(
            "Usuário atualizado com sucesso.",
            "success"
        )

        origem = request.form.get(
            "origem"
        )

        if origem == "completo":

            return redirect(
                url_for("usuario.completo")
            )

        return redirect(
            url_for("usuario.listar")
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

    usuario = Usuario.query.get_or_404(
        id_usuario
    )

    usuario.ativo = not usuario.ativo

    db.session.commit()

    flash(
        "Status do usuário atualizado.",
        "success"
    )

    origem = request.args.get(
        "origem"
    )

    if origem == "completo":

        return redirect(
            url_for("usuario.completo")
        )

    return redirect(
        url_for("usuario.listar")
    )


@usuario_bp.route(
    "/<int:id_usuario>"
)
@requer_perfil("Administrador")
def detalhes(id_usuario):

    usuario = Usuario.query.get_or_404(
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

    usuarios = UsuarioService.listar(
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


@usuario_bp.route("/meu-perfil", methods=["GET", "POST"])
@requer_perfil("Administrador","Operador","Leitor")
def meu_perfil():

    usuario = Usuario.query.get_or_404(
        session["usuario_id"]
    )

    if request.method == "POST":

        # =====================================================
        # ALTERAÇÕES ADMINISTRATIVAS
        # SOMENTE ADMINISTRADOR
        # =====================================================

        if session.get("perfil") == "Administrador":

            nome = request.form["nome"].strip()
            login = request.form["login"].strip()
            perfil = request.form["perfil"].strip()

            if not nome:

                flash(
                    "Informe o nome.",
                    "warning"
                )

                return render_template(
                    "usuarios/meu_perfil.html",
                    titulo="Meu Perfil",
                    usuario=usuario
                )

            if not login:

                flash(
                    "Informe o login.",
                    "warning"
                )

                return render_template(
                    "usuarios/meu_perfil.html",
                    titulo="Meu Perfil",
                    usuario=usuario
                )

            if perfil not in [
                "Administrador",
                "Operador",
                "Leitor"
            ]:

                flash(
                    "Perfil inválido.",
                    "warning"
                )

                return render_template(
                    "usuarios/meu_perfil.html",
                    titulo="Meu Perfil",
                    usuario=usuario
                )

            usuario_existente = Usuario.query.filter(
                Usuario.login.ilike(login),
                Usuario.id_usuario != usuario.id_usuario
            ).first()

            if usuario_existente:

                flash(
                    "Já existe um usuário com esse login.",
                    "warning"
                )

                usuario.nome = nome
                usuario.login = login
                usuario.perfil = perfil

                return render_template(
                    "usuarios/meu_perfil.html",
                    titulo="Meu Perfil",
                    usuario=usuario
                )

            usuario.nome = nome
            usuario.login = login
            usuario.perfil = perfil

        # =====================================================
        # ALTERAÇÃO DE SENHA
        # TODOS OS PERFIS
        # =====================================================

        senha_atual = (
            request.form["senha_atual"].strip()
        )

        nova_senha = (
            request.form["nova_senha"].strip()
        )

        confirmar_senha = (
            request.form["confirmar_senha"].strip()
        )

        if not senha_atual:

            flash(
                "Informe a senha atual.",
                "warning"
            )

            return render_template(
                "usuarios/meu_perfil.html",
                titulo="Meu Perfil",
                usuario=usuario
            )

        if not usuario.verificar_senha(
            senha_atual
        ):

            flash(
                "Senha atual incorreta.",
                "warning"
            )

            return render_template(
                "usuarios/meu_perfil.html",
                titulo="Meu Perfil",
                usuario=usuario
            )

        if not nova_senha:

            flash(
                "Informe a nova senha.",
                "warning"
            )

            return render_template(
                "usuarios/meu_perfil.html",
                titulo="Meu Perfil",
                usuario=usuario
            )

        if nova_senha != confirmar_senha:

            flash(
                "A confirmação da nova senha não confere.",
                "warning"
            )

            return render_template(
                "usuarios/meu_perfil.html",
                titulo="Meu Perfil",
                usuario=usuario
            )

        if senha_atual == nova_senha:

            flash(
                "A nova senha deve ser diferente da senha atual.",
                "warning"
            )

            return render_template(
                "usuarios/meu_perfil.html",
                titulo="Meu Perfil",
                usuario=usuario
            )

        usuario.set_senha(
            nova_senha
        )

        db.session.commit()

        # =====================================================
        # ATUALIZA DADOS DA SESSÃO
        # CASO O ADMINISTRADOR TENHA ALTERADO OS DADOS
        # =====================================================

        session["usuario_nome"] = usuario.nome
        session["perfil"] = usuario.perfil

        flash(
            "Perfil atualizado com sucesso.",
            "success"
        )

        return redirect(
            url_for("usuario.meu_perfil")
        )

    return render_template(
        "usuarios/meu_perfil.html",
        titulo="Meu Perfil",
        usuario=usuario
    )