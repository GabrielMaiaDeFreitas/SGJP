from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)


from app import db
from app.models import Motorista

from datetime import datetime

motorista_bp = Blueprint(
    "motorista",
    __name__,
    url_prefix="/motoristas"
)

@motorista_bp.route("/")
def listar():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    motoristas = Motorista.query.order_by(
        Motorista.nome
    ).all()

    return render_template(
        "motoristas/listar.html",
        motoristas=motoristas,
        titulo="Gerenciamento de Motoristas"
    )

@motorista_bp.route("/novo", methods=["GET", "POST"])
def novo():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    if request.method == "POST":

        motorista = Motorista(

            matricula=request.form["matricula"],

            nome=request.form["nome"],

            numero_cnh=request.form["numero_cnh"],

            categoria_cnh=request.form["categoria_cnh"],

            validade_cnh=datetime.strptime(
                request.form["validade_cnh"],
                "%Y-%m-%d"
            ).date(),

            validade_toxicologico=datetime.strptime(
                request.form["validade_toxicologico"],
                "%Y-%m-%d"
            ).date(),

            ativo=True

        )

        db.session.add(motorista)

        db.session.commit()

        flash(
            "Motorista cadastrado com sucesso.",
            "success"
        )

        return redirect(
            url_for("motorista.listar")
        )

    return render_template(
        "motoristas/form.html",
        titulo="Novo Motorista",
        motorista=None
    )

@motorista_bp.route("/<int:id_motorista>")
def detalhes(id_motorista):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    motorista = Motorista.query.get_or_404(id_motorista)

    return render_template(
        "motoristas/detalhes.html",
        motorista=motorista,
        titulo="Detalhes do Motorista"
    )


@motorista_bp.route("/<int:id_motorista>/editar", methods=["GET", "POST"])
def editar(id_motorista):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    motorista = Motorista.query.get_or_404(id_motorista)

    if request.method == "POST":

        motorista.matricula = request.form["matricula"]
        motorista.nome = request.form["nome"]
        motorista.numero_cnh = request.form["numero_cnh"]
        motorista.categoria_cnh = request.form["categoria_cnh"]

        motorista.validade_cnh = datetime.strptime(
            request.form["validade_cnh"],
            "%Y-%m-%d"
        ).date()

        motorista.validade_toxicologico = datetime.strptime(
            request.form["validade_toxicologico"],
            "%Y-%m-%d"
        ).date()

        db.session.commit()

        flash(
            "Motorista atualizado com sucesso.",
            "success"
        )

        origem = request.form.get("origem")

        if origem == "completo":
            return redirect(url_for("motorista.completo"))

        return redirect(url_for("motorista.listar"))

    origem = request.args.get("origem")

    return render_template(
        "motoristas/form.html",
        titulo="Editar Motorista",
        motorista=motorista,
        origem=origem
    )

@motorista_bp.route("/<int:id_motorista>/toggle")
def toggle(id_motorista):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    motorista = Motorista.query.get_or_404(id_motorista)

    motorista.ativo = not motorista.ativo

    db.session.commit()

    flash(
        "Status do motorista atualizado.",
        "success"
    )

    origem = request.args.get("origem")

    if origem == "completo":
        return redirect(url_for("motorista.completo"))

    return redirect(url_for("motorista.listar"))

@motorista_bp.route("/completo")
def completo():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    motoristas = Motorista.query.order_by(
        Motorista.nome
    ).all()

    return render_template(
        "motoristas/completo.html",
        titulo="Visualização Completa de Motoristas",
        motoristas=motoristas
    )