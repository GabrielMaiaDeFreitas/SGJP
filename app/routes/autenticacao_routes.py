from flask import (Blueprint, flash, redirect, render_template, request,session, url_for)
from app.models import Usuario

autenticacao_bp = Blueprint("autenticacao",__name__)

@autenticacao_bp.route("/", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        login = request.form["login"]
        senha = request.form["senha"]
        usuario = Usuario.query.filter_by(login=login).first()

        if usuario is None:
            flash("Usuário não encontrado.","danger")
            return redirect(url_for("autenticacao.login"))

        if not usuario.ativo:
            flash("Usuário desativado.","warning" )
            return redirect(url_for("autenticacao.login"))

        if not usuario.verificar_senha(senha):
            flash("Senha incorreta.","danger")
            return redirect(url_for("autenticacao.login"))

        session["usuario_id"] = usuario.id_usuario
        session["usuario_nome"] = usuario.nome
        session["perfil"] = usuario.perfil
        return redirect(url_for("dashboard.dashboard"))

    return render_template("autenticacao/login.html")

@autenticacao_bp.route("/logout")
def logout():

    session.clear()

    flash("Logout realizado com sucesso.","success")

    return redirect(
        url_for("autenticacao.login")
    )