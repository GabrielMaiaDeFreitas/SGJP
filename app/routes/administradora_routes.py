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
from app.models import Administradora
from app.filters.administradora import FILTROS_ADMINISTRADORA
from app.services.administradora_service import AdministradoraService


administradora_bp = Blueprint(
    "administradora",
    __name__,
    url_prefix="/administradoras"
)


@administradora_bp.route("/")
def listar():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    administradoras = Administradora.query.order_by(
        Administradora.nome
    ).all()

    return render_template(

        "administradoras/listar.html",

        titulo="Gerenciamento de Administradoras",

        administradoras=administradoras,

        novo_url=url_for("administradora.novo"),

        novo_texto="Nova Administradora",

        visualizacao_url=url_for("administradora.completo"),

        exportar_url=url_for(
            "exportacao.exportar_generico",
            modulo="administradora"
        )

    )


@administradora_bp.route("/novo", methods=["GET", "POST"])
def novo():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    if request.method == "POST":

        if Administradora.query.filter(
            Administradora.nome.ilike(
                request.form["nome"]
            )
        ).first():

            flash(
                "Já existe uma administradora com esse nome.",
                "warning"
            )

            administradora = Administradora(
                nome=request.form["nome"],
                cliente_proprio=(
                    request.form.get("cliente_proprio")
                    == "Sim"
                )
            )

            return render_template(
                "administradoras/form.html",
                titulo="Nova Administradora",
                administradora=administradora
            )

        administradora = Administradora(

            nome=request.form["nome"],

            cliente_proprio=(
                request.form.get("cliente_proprio")
                == "Sim"
            ),

            ativo=True

        )

        db.session.add(administradora)
        db.session.commit()

        flash(
            "Administradora cadastrada com sucesso.",
            "success"
        )

        if administradora.cliente_proprio:

            return redirect(

                url_for(

                    "cliente.novo",

                    id_administradora=(
                        administradora.id_administradora
                    ),

                    origem="administradora"

                )

            )

        return redirect(
            url_for("administradora.listar")
        )

    return render_template(

        "administradoras/form.html",

        titulo="Nova Administradora",

        administradora=None

    )


@administradora_bp.route("/<int:id_administradora>/editar", methods=["GET", "POST"])
def editar(id_administradora):

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    administradora = Administradora.query.get_or_404(
        id_administradora
    )

    if request.method == "POST":

        administradora_existente = Administradora.query.filter(
            Administradora.nome.ilike(
                request.form["nome"]
            ),
            Administradora.id_administradora != id_administradora
        ).first()

        if administradora_existente:

            flash(
                "Já existe uma administradora com esse nome.",
                "warning"
            )

            administradora.nome = request.form["nome"]

            administradora.cliente_proprio = (
                request.form.get("cliente_proprio")
                == "Sim"
            )

            return render_template(

                "administradoras/form.html",

                titulo="Editar Administradora",

                administradora=administradora,

                origem=request.args.get("origem")

            )

        administradora.nome = request.form["nome"]

        administradora.cliente_proprio = (
            request.form.get("cliente_proprio")
            == "Sim"
        )

        db.session.commit()

        flash(
            "Administradora atualizada com sucesso.",
            "success"
        )

        origem = request.form.get("origem")

        if origem == "completo":
            return redirect(
                url_for("administradora.completo")
            )

        return redirect(
            url_for("administradora.listar")
        )

    return render_template(

        "administradoras/form.html",

        titulo="Editar Administradora",

        administradora=administradora,

        origem=request.args.get("origem")

    )


@administradora_bp.route("/<int:id_administradora>/toggle")
def toggle(id_administradora):

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    administradora = Administradora.query.get_or_404(
        id_administradora
    )

    administradora.ativo = not administradora.ativo

    db.session.commit()

    flash(
        "Status da administradora atualizado.",
        "success"
    )

    origem = request.args.get("origem")

    if origem == "completo":
        return redirect(
            url_for("administradora.completo")
        )

    return redirect(
        url_for("administradora.listar")
    )


@administradora_bp.route("/<int:id_administradora>")
def detalhes(id_administradora):

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    administradora = Administradora.query.get_or_404(
        id_administradora
    )

    return render_template(

        "administradoras/detalhes.html",

        titulo="Detalhes da Administradora",

        administradora=administradora

    )


@administradora_bp.route("/completo")
def completo():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    ordem_final = (
        request.args.get("ordenar_por")
        or "nome"
    )

    administradoras = AdministradoraService.listar(
        request.args
    )

    return render_template(

        "administradoras/completo.html",

        titulo="Visualização Completa de Administradoras",

        administradoras=administradoras,

        campos=FILTROS_ADMINISTRADORA,

        campos_filtro=request.args.getlist("campo[]"),

        valores_filtro=request.args.getlist("valor[]")

    )