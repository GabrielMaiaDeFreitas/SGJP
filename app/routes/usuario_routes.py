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
        usuarios=usuarios
    )

@usuario_bp.route("/novo", methods=["GET", "POST"])
def novo():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    if request.method == "POST":

        usuario = Usuario(
            nome=request.form["nome"],
            login=request.form["login"],
            perfil=request.form["perfil"],
            ativo=True
        )

        usuario.set_senha(request.form["senha"])

        db.session.add(usuario)
        db.session.commit()

        flash(
            "Usuário cadastrado com sucesso.",
            "success"
        )

        return redirect(url_for("usuario.listar"))

    return render_template(
        "usuarios/form.html",
        titulo="Novo Usuário",
        usuario=None
    )

@usuario_bp.route("/<int:id_usuario>/editar", methods=["GET", "POST"])
def editar(id_usuario):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    usuario = Usuario.query.get_or_404(id_usuario)

    if request.method == "POST":

        usuario.nome = request.form["nome"]
        usuario.login = request.form["login"]
        usuario.perfil = request.form["perfil"]

        senha = request.form["senha"].strip()

        if senha:
            usuario.set_senha(senha)

        db.session.commit()

        flash(
            "Usuário atualizado com sucesso.",
            "success"
        )

        return redirect(
            url_for("usuario.listar")
        )

    return render_template(
        "usuarios/form.html",
        titulo="Editar Usuário",
        usuario=usuario
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

    return redirect(
        url_for("usuario.listar")
    )