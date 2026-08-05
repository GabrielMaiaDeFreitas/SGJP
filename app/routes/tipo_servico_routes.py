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
from app.models import TipoServico
from app.filters.tipo_servico import FILTROS_TIPO_SERVICO
from app.services.tipo_servico_service import TipoServicoService


tipo_servico_bp = Blueprint(
    "tipo_servico",
    __name__,
    url_prefix="/tipos-servico"
)


@tipo_servico_bp.route("/")
def listar():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    tipos_servico = TipoServico.query.order_by(
        TipoServico.nome
    ).all()

    return render_template(

        "tipos_servico/listar.html",

        titulo="Gerenciamento de Tipos de Serviço",

        tipos_servico=tipos_servico,

        novo_url=url_for("tipo_servico.novo"),

        novo_texto="Novo Tipo de Serviço",

        visualizacao_url=url_for("tipo_servico.completo"),

        exportar_url=url_for(
            "exportacao.exportar_generico",
            modulo="tipo_servico"
        )

    )


@tipo_servico_bp.route("/novo", methods=["GET", "POST"])
def novo():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    if request.method == "POST":

        def voltar_formulario():

            tipo_servico = TipoServico(
                nome=request.form["nome"]
            )

            return render_template(

                "tipos_servico/form.html",

                titulo="Novo Tipo de Serviço",

                tipo_servico=tipo_servico

            )

        if TipoServico.query.filter(
            TipoServico.nome.ilike(request.form["nome"])
        ).first():

            flash(
                "Já existe um tipo de serviço com esse nome.",
                "warning"
            )

            return voltar_formulario()

        tipo_servico = TipoServico(

            nome=request.form["nome"],

            ativo=True

        )

        db.session.add(tipo_servico)

        db.session.commit()

        flash(
            "Tipo de serviço cadastrado com sucesso.",
            "success"
        )

        return redirect(
            url_for("tipo_servico.listar")
        )

    return render_template(

        "tipos_servico/form.html",

        titulo="Novo Tipo de Serviço",

        tipo_servico=None

    )


@tipo_servico_bp.route("/<int:id_tipo_servico>/editar", methods=["GET", "POST"])
def editar(id_tipo_servico):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    tipo_servico = TipoServico.query.get_or_404(
        id_tipo_servico
    )

    if request.method == "POST":

        def voltar_formulario():

            tipo_servico.nome = request.form["nome"]

            return render_template(

                "tipos_servico/form.html",

                titulo="Editar Tipo de Serviço",

                tipo_servico=tipo_servico,

                origem=request.args.get("origem")

            )

        existente = TipoServico.query.filter(

            TipoServico.nome == request.form["nome"],

            TipoServico.id_tipo_servico != id_tipo_servico

        ).first()

        if existente:

            flash(
                "Já existe um tipo de serviço com esse nome.",
                "warning"
            )

            return voltar_formulario()

        tipo_servico.nome = request.form["nome"]

        db.session.commit()

        flash(
            "Tipo de serviço atualizado com sucesso.",
            "success"
        )

        origem = request.form.get("origem")

        if origem == "completo":

            return redirect(
                url_for("tipo_servico.completo")
            )

        return redirect(
            url_for("tipo_servico.listar")
        )

    return render_template(

        "tipos_servico/form.html",

        titulo="Editar Tipo de Serviço",

        tipo_servico=tipo_servico,

        origem=request.args.get("origem")

    )


@tipo_servico_bp.route("/<int:id_tipo_servico>/toggle")
def toggle(id_tipo_servico):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    tipo_servico = TipoServico.query.get_or_404(
        id_tipo_servico
    )

    tipo_servico.ativo = not tipo_servico.ativo

    db.session.commit()

    flash(
        "Status atualizado com sucesso.",
        "success"
    )

    origem = request.args.get("origem")

    if origem == "completo":

        return redirect(
            url_for("tipo_servico.completo")
        )

    return redirect(
        url_for("tipo_servico.listar")
    )


@tipo_servico_bp.route("/<int:id_tipo_servico>")
def detalhes(id_tipo_servico):

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    tipo_servico = TipoServico.query.get_or_404(
        id_tipo_servico
    )

    return render_template(

        "tipos_servico/detalhes.html",

        titulo="Detalhes do Tipo de Serviço",

        tipo_servico=tipo_servico

    )


@tipo_servico_bp.route("/completo")
def completo():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    tipos_servico = TipoServicoService.listar(
        request.args
    )

    return render_template(

        "tipos_servico/completo.html",

        titulo="Visualização Completa de Tipos de Serviço",

        tipos_servico=tipos_servico,

        campos=FILTROS_TIPO_SERVICO,

        campos_filtro=request.args.getlist("campo[]"),

        valores_filtro=request.args.getlist("valor[]")

    )