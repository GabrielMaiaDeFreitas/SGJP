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
from app.services.filter_service import FilterService


usuario_bp = Blueprint(
    "usuario",
    __name__,
    url_prefix="/usuarios"
)


@usuario_bp.route("/")
def listar():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    usuarios = Usuario.query.order_by(
        Usuario.nome
    ).all()

    return render_template(
    "usuarios/listar.html",
    titulo="Gerenciamento de Usuários",
    usuarios=usuarios,
    novo_url=url_for("usuario.novo"),
    novo_texto="Novo Usuário",
    visualizacao_url=url_for("usuario.completo"),
    exportar_url=url_for(
        "exportacao.exportar_generico",
        modulo="usuario"
    )
)

@usuario_bp.route("/novo", methods=["GET", "POST"])
def novo():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

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
        confirmar_senha = request.form["confirmar_senha"].strip()

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

        if Usuario.query.filter(Usuario.login.ilike(request.form["login"])).first():
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

@usuario_bp.route("/<int:id_usuario>/editar", methods=["GET", "POST"])
def editar(id_usuario):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    usuario = Usuario.query.get_or_404(id_usuario)

    if request.method == "POST":

        def voltar_formulario():

            usuario.nome = request.form["nome"]
            usuario.login = request.form["login"]
            usuario.perfil = request.form["perfil"]

            return render_template(

                "usuarios/form.html",

                titulo="Novo Usuário",

                usuario=usuario,

                editando=True

            )

        usuario_existente = Usuario.query.filter(
            Usuario.login.ilike(request.form["login"]),
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

        senha_atual = request.form["senha_atual"].strip()
        nova_senha = request.form["nova_senha"].strip()
        confirmar_senha = request.form["confirmar_senha"].strip()

        if senha_atual or nova_senha or confirmar_senha:

            if not senha_atual:

                flash(
                    "Informe a senha atual.",
                    "warning"
                )

                return voltar_formulario()

            if not usuario.verificar_senha(senha_atual):

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

            usuario.set_senha(nova_senha)

        db.session.commit()

        flash(
            "Usuário atualizado com sucesso.",
            "success"
        )

        origem = request.form.get("origem")

        if origem == "completo":
            return redirect(url_for("usuario.completo"))

        return redirect(url_for("usuario.listar"))

    return render_template(
        "usuarios/form.html",
        titulo="Editar Usuário",
        usuario=usuario,
        editando=True,
        origem=request.args.get("origem")
    )

@usuario_bp.route("/<int:id_usuario>/toggle")
def toggle(id_usuario):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    usuario = Usuario.query.get_or_404(id_usuario)

    usuario.ativo = not usuario.ativo

    db.session.commit()

    flash(
        "Status do usuário atualizado.",
        "success"
    )

    origem = request.args.get("origem")

    if origem == "completo":
        return redirect(url_for("usuario.completo"))

    return redirect(url_for("usuario.listar"))

@usuario_bp.route("/<int:id_usuario>")
def detalhes(id_usuario):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    usuario = Usuario.query.get_or_404(id_usuario)

    return render_template(
        "usuarios/detalhes.html",
        titulo="Detalhes do Usuário",
        usuario=usuario
    )

@usuario_bp.route("/completo")
def completo():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    ordem_final = (
        request.args.get("ordenar_por")
        or "nome"
    )

    usuarios = FilterService.listar(

        modelo=Usuario,

        filtros=request.args,

        configuracoes=FILTROS_USUARIO,

        ordenar_por=ordem_final

    )

    return render_template(

        "usuarios/completo.html",

        titulo="Visualização Completa de Usuários",

        usuarios=usuarios,

        campos=FILTROS_USUARIO,

        campos_filtro=request.args.getlist("campo[]"),

        valores_filtro=request.args.getlist("valor[]")

    )