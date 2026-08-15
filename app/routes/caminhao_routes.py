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
from app.models import Caminhao
from app.filters.caminhao import FILTROS_CAMINHAO
from app.services.caminhao_service import CaminhaoService

from app.helpers.autorizacao_helper import (proteger_blueprint)


caminhao_bp = Blueprint(
    "caminhao",
    __name__,
    url_prefix="/caminhoes"
)

proteger_blueprint(caminhao_bp,"Administrador")

@caminhao_bp.route("/")
def listar():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    caminhoes = Caminhao.query.order_by(
        Caminhao.modelo
    ).all()

    return render_template(
        "caminhoes/listar.html",
        titulo="Gerenciamento de Caminhões",
        caminhoes=caminhoes,
        novo_url=url_for("caminhao.novo"),
        novo_texto="Novo Caminhão",
        visualizacao_url=url_for("caminhao.completo"),
        exportar_url = url_for("exportacao.exportar_generico",modulo="caminhao")
    )

@caminhao_bp.route("/novo", methods=["GET", "POST"])
def novo():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    if request.method == "POST":

        caminhao = Caminhao(

            placa=request.form["placa"],
            modelo=request.form["modelo"]

        )

        db.session.add(caminhao)
        db.session.commit()

        flash(
            "Caminhão cadastrado com sucesso.",
            "success"
        )

        return redirect(
            url_for("caminhao.listar")
        )

    return render_template(

        "caminhoes/form.html",

        titulo="Novo Caminhão",

        caminhao=None

    )

@caminhao_bp.route("/<int:id_caminhao>/editar", methods=["GET", "POST"])
def editar(id_caminhao):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    caminhao = Caminhao.query.get_or_404(id_caminhao)

    if request.method == "POST":

        caminhao.placa = request.form["placa"]
        caminhao.modelo = request.form["modelo"]

        db.session.commit()

        flash(
            "Caminhão atualizado com sucesso.",
            "success"
        )

        origem = request.form.get("origem")

        if origem == "completo":
            return redirect(url_for("caminhao.completo"))

        return redirect(url_for("caminhao.listar"))

    return render_template(
        "caminhoes/form.html",
        titulo="Editar Caminhão",
        caminhao=caminhao,
        origem=request.args.get("origem")
    )

@caminhao_bp.route("/<int:id_caminhao>/toggle")
def toggle(id_caminhao):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    caminhao = Caminhao.query.get_or_404(id_caminhao)

    caminhao.ativo = not caminhao.ativo

    db.session.commit()

    flash(
        "Status do caminhão atualizado.",
        "success"
    )

    origem = request.args.get("origem")

    if origem == "completo":
        return redirect(url_for("caminhao.completo"))

    return redirect(url_for("caminhao.listar"))

@caminhao_bp.route("/<int:id_caminhao>")
def detalhes(id_caminhao):

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    caminhao = Caminhao.query.get_or_404(
        id_caminhao
    )

    return render_template(
        "caminhoes/detalhes.html",
        titulo="Detalhes do Caminhão",
        caminhao=caminhao
    )

@caminhao_bp.route("/completo")
def completo():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    caminhoes = CaminhaoService.listar(
        request.args
    )

    return render_template(
        "caminhoes/completo.html",
        titulo="Visualização Completa de Caminhões",
        caminhoes=caminhoes,
        campos=FILTROS_CAMINHAO,
        campos_filtro=request.args.getlist("campo[]"),
        valores_filtro=request.args.getlist("valor[]")
    )

