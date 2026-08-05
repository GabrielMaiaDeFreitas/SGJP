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

from app.models import (
    Cliente,
    Administradora
)

from app.filters.cliente import FILTROS_CLIENTE
from app.services.cliente_service import ClienteService


cliente_bp = Blueprint(
    "cliente",
    __name__,
    url_prefix="/clientes"
)


@cliente_bp.route("/")
def listar():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    clientes = Cliente.query.order_by(
        Cliente.nome_fantasia
    ).all()

    return render_template(

        "clientes/listar.html",

        titulo="Gerenciamento de Clientes",

        clientes=clientes,

        novo_url=url_for("cliente.novo"),

        novo_texto="Novo Cliente",

        visualizacao_url=url_for("cliente.completo"),

        exportar_url=url_for(
            "exportacao.exportar_generico",
            modulo="cliente"
        )

    )


@cliente_bp.route("/novo", methods=["GET", "POST"])
def novo():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    administradoras = Administradora.query.filter_by(

        ativo=True,

        cliente_proprio=False

    ).order_by(

        Administradora.nome

    ).all()

    if request.method == "POST":

        def voltar_formulario():

            cliente = Cliente(

                nome_fantasia=request.form["nome_fantasia"],

                razao_social=request.form["razao_social"],

                cnpj=request.form["cnpj"],

                fk_administradora_id_administradora=request.form[
                    "fk_administradora_id_administradora"
                ]

            )

            return render_template(

                "clientes/form.html",

                titulo="Novo Cliente",

                cliente=cliente,

                administradoras=administradoras

            )

        if Cliente.query.filter(

            Cliente.cnpj == request.form["cnpj"]

        ).first():

            flash(
                "Já existe um cliente com esse CNPJ.",
                "warning"
            )

            return voltar_formulario()

        cliente = Cliente(

            nome_fantasia=request.form["nome_fantasia"],

            razao_social=request.form["razao_social"],

            cnpj=request.form["cnpj"],

            ativo=True,

            fk_administradora_id_administradora=request.form[
                "fk_administradora_id_administradora"
            ]

        )

        db.session.add(cliente)

        db.session.commit()

        flash(
            "Cliente cadastrado com sucesso.",
            "success"
        )

        return redirect(
            url_for("cliente.listar")
        )

    return render_template(

        "clientes/form.html",

        titulo="Novo Cliente",

        cliente=None,

        administradoras=administradoras

    )


@cliente_bp.route("/<int:id_cliente>/editar", methods=["GET", "POST"])
def editar(id_cliente):

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    cliente = Cliente.query.get_or_404(id_cliente)

    administradoras = Administradora.query.filter_by(

        ativo=True,

        cliente_proprio=False

    ).order_by(

        Administradora.nome

    ).all()

    if request.method == "POST":

        def voltar_formulario():

            cliente.nome_fantasia = request.form["nome_fantasia"]
            cliente.razao_social = request.form["razao_social"]
            cliente.cnpj = request.form["cnpj"]
            cliente.fk_administradora_id_administradora = request.form[
                "fk_administradora_id_administradora"
            ]

            return render_template(

                "clientes/form.html",

                titulo="Editar Cliente",

                cliente=cliente,

                administradoras=administradoras,

                origem=request.args.get("origem")

            )

        existente = Cliente.query.filter(

            Cliente.cnpj == request.form["cnpj"],

            Cliente.id_cliente != id_cliente

        ).first()

        if existente:

            flash(
                "Já existe um cliente com esse CNPJ.",
                "warning"
            )

            return voltar_formulario()

        cliente.nome_fantasia = request.form["nome_fantasia"]
        cliente.razao_social = request.form["razao_social"]
        cliente.cnpj = request.form["cnpj"]
        cliente.fk_administradora_id_administradora = request.form[
            "fk_administradora_id_administradora"
        ]

        db.session.commit()

        flash(
            "Cliente atualizado com sucesso.",
            "success"
        )

        origem = request.form.get("origem")

        if origem == "completo":

            return redirect(
                url_for("cliente.completo")
            )

        return redirect(
            url_for("cliente.listar")
        )

    return render_template(

        "clientes/form.html",

        titulo="Editar Cliente",

        cliente=cliente,

        administradoras=administradoras,

        origem=request.args.get("origem")

    )


@cliente_bp.route("/<int:id_cliente>/toggle")
def toggle(id_cliente):

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    cliente = Cliente.query.get_or_404(id_cliente)

    cliente.ativo = not cliente.ativo

    db.session.commit()

    flash(
        "Status atualizado com sucesso.",
        "success"
    )

    origem = request.args.get("origem")

    if origem == "completo":

        return redirect(
            url_for("cliente.completo")
        )

    return redirect(
        url_for("cliente.listar")
    )


@cliente_bp.route("/<int:id_cliente>")
def detalhes(id_cliente):

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    cliente = Cliente.query.get_or_404(id_cliente)

    return render_template(

        "clientes/detalhes.html",

        titulo="Detalhes do Cliente",

        cliente=cliente

    )


@cliente_bp.route("/completo")
def completo():

    if "usuario_id" not in session:
        return redirect(
            url_for("autenticacao.login")
        )

    clientes = ClienteService.listar(
        request.args
    )

    return render_template(

        "clientes/completo.html",

        titulo="Visualização Completa de Clientes",

        clientes=clientes,

        campos=FILTROS_CLIENTE,

        campos_filtro=request.args.getlist("campo[]"),

        valores_filtro=request.args.getlist("valor[]")

    )