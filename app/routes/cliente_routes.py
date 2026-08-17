from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

from app.models import Administradora

from app.filters.cliente import (
    FILTROS_CLIENTE
)

from app.services.cliente_service import (
    ClienteService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)

from copy import deepcopy


cliente_bp = Blueprint(
    "cliente",
    __name__,
    url_prefix="/clientes"
)


proteger_blueprint(
    cliente_bp,
    "Administrador"
)


@cliente_bp.route("/")
def listar():

    clientes = ClienteService.listar()


    return render_template(

        "clientes/listar.html",

        titulo="Gerenciamento de Clientes",

        clientes=clientes,

        novo_url=url_for(
            "cliente.novo"
        ),

        novo_texto="Novo Cliente",

        visualizacao_url=url_for(
            "cliente.completo"
        ),

        exportar_url=url_for(

            "exportacao.exportar_generico",

            modulo="cliente"

        )

    )


@cliente_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
def novo():

    origem = request.args.get(
        "origem"
    )

    id_administradora = request.args.get(
        "id_administradora",
        type=int
    )


    administradoras = (
        _obter_administradoras(
            origem
        )
    )


    if request.method == "POST":

        nome_fantasia = request.form.get(
            "nome_fantasia"
        )

        razao_social = request.form.get(
            "razao_social"
        )

        cnpj = request.form.get(
            "cnpj"
        )

        id_administradora = request.form.get(
            "fk_administradora_id_administradora",
            type=int
        )


        try:

            cliente = ClienteService.criar(

                nome_fantasia=nome_fantasia,

                razao_social=razao_social,

                cnpj=cnpj,

                id_administradora=
                    id_administradora,

                origem=request.form.get(
                    "origem"
                )

            )

        except (
            CampoObrigatorioError,
            RecursoDuplicadoError,
            ValidacaoError
        ) as erro:

            flash(
                erro.mensagem,
                "warning"
            )


            cliente = _cliente_formulario(

                nome_fantasia,

                razao_social,

                cnpj,

                id_administradora

            )


            return render_template(

                "clientes/form.html",

                titulo="Novo Cliente",

                cliente=cliente,

                administradoras=administradoras,

                origem=request.form.get(
                    "origem"
                )

            )


        flash(

            "Cliente cadastrado com sucesso.",

            "success"

        )


        return redirect(

            url_for(
                "cliente.listar"
            )

        )


    cliente = None


    if (
        origem == "administradora"
        and id_administradora
    ):

        administradora = (
            Administradora.query.get_or_404(
                id_administradora
            )
        )


        cliente = _cliente_formulario(

            administradora.nome,

            "",

            "",

            administradora.id_administradora

        )


    return render_template(

        "clientes/form.html",

        titulo="Novo Cliente",

        cliente=cliente,

        administradoras=administradoras,

        origem=origem

    )


@cliente_bp.route(
    "/<int:id_cliente>/editar",
    methods=["GET", "POST"]
)
def editar(id_cliente):

    cliente = ClienteService.buscar_por_id(
        id_cliente
    )


    administradoras = (
        _obter_administradoras()
    )


    if request.method == "POST":

        try:

            ClienteService.atualizar(

                cliente=cliente,

                nome_fantasia=
                    request.form.get(
                        "nome_fantasia"
                    ),

                razao_social=
                    request.form.get(
                        "razao_social"
                    ),

                cnpj=
                    request.form.get(
                        "cnpj"
                    ),

                id_administradora=
                    request.form.get(
                        "fk_administradora_id_administradora",
                        type=int
                    )

            )

        except (
            CampoObrigatorioError,
            RecursoDuplicadoError,
            ValidacaoError
        ) as erro:

            flash(
                erro.mensagem,
                "warning"
            )


            cliente.nome_fantasia = (
                request.form.get(
                    "nome_fantasia"
                )
                or ""
            )

            cliente.razao_social = (
                request.form.get(
                    "razao_social"
                )
                or ""
            )

            cliente.cnpj = (
                request.form.get(
                    "cnpj"
                )
                or ""
            )


            return render_template(

                "clientes/form.html",

                titulo="Editar Cliente",

                cliente=cliente,

                administradoras=administradoras,

                origem=request.form.get(
                    "origem"
                )

            )


        flash(

            "Cliente atualizado com sucesso.",

            "success"

        )


        if request.form.get(
            "origem"
        ) == "completo":

            return redirect(

                url_for(
                    "cliente.completo"
                )

            )


        return redirect(

            url_for(
                "cliente.listar"
            )

        )


    return render_template(

        "clientes/form.html",

        titulo="Editar Cliente",

        cliente=cliente,

        administradoras=administradoras,

        origem=request.args.get(
            "origem"
        )

    )


@cliente_bp.route(
    "/<int:id_cliente>/toggle"
)
def toggle(id_cliente):

    cliente = ClienteService.buscar_por_id(
        id_cliente
    )


    ClienteService.alternar_status(
        cliente
    )


    flash(

        "Status atualizado com sucesso.",

        "success"

    )


    if request.args.get(
        "origem"
    ) == "completo":

        return redirect(

            url_for(
                "cliente.completo"
            )

        )


    return redirect(

        url_for(
            "cliente.listar"
        )

    )


@cliente_bp.route(
    "/<int:id_cliente>"
)
def detalhes(id_cliente):

    cliente = ClienteService.buscar_por_id(
        id_cliente
    )


    return render_template(

        "clientes/detalhes.html",

        titulo="Detalhes do Cliente",

        cliente=cliente

    )


@cliente_bp.route(
    "/completo"
)
def completo():

    clientes = (
        ClienteService.listar_completo(
            request.args
        )
    )


    campos = deepcopy(
        FILTROS_CLIENTE
    )


    administradoras = (
        Administradora.query.filter_by(

            ativo=True

        ).order_by(

            Administradora.nome

        ).all()
    )


    for campo in campos:

        if (
            campo["campo"]
            == "fk_administradora_id_administradora"
        ):

            campo["opcoes"] = [

                {
                    "id":
                        administradora.id_administradora,

                    "label":
                        administradora.nome
                }

                for administradora
                in administradoras

            ]


    return render_template(

        "clientes/completo.html",

        titulo="Visualização Completa de Clientes",

        clientes=clientes,

        campos=campos,

        campos_filtro=request.args.getlist(
            "campo[]"
        ),

        valores_filtro=request.args.getlist(
            "valor[]"
        )

    )


@cliente_bp.route(
    "/cancelar-cadastro-proprio/<int:id_administradora>"
)
def cancelar_cadastro_proprio(
    id_administradora
):

    ClienteService.cancelar_cadastro_proprio(
        id_administradora
    )


    flash(
        "Cadastro cancelado.",
        "info"
    )


    return redirect(

        url_for(
            "administradora.listar"
        )

    )


# =========================================================
# AUXILIARES
# =========================================================

def _obter_administradoras(
    origem=None
):

    if origem == "administradora":

        return Administradora.query.filter_by(

            ativo=True

        ).order_by(

            Administradora.nome

        ).all()


    return Administradora.query.filter_by(

        ativo=True,

        cliente_proprio=False

    ).order_by(

        Administradora.nome

    ).all()


def _cliente_formulario(
    nome_fantasia,
    razao_social,
    cnpj,
    id_administradora
):

    from app.models import Cliente

    return Cliente(

        nome_fantasia=
            nome_fantasia or "",

        razao_social=
            razao_social or "",

        cnpj=
            cnpj or "",

        fk_administradora_id_administradora=
            id_administradora

    )