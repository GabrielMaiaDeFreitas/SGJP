from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.filters.administradora import (
    FILTROS_ADMINISTRADORA
)

from app.services.administradora_service import (
    AdministradoraService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)


administradora_bp = Blueprint(

    "administradora",

    __name__,

    url_prefix="/administradoras"

)


proteger_blueprint(
    administradora_bp,
    "Administrador"
)


@administradora_bp.route("/")
def listar():

    administradoras = (
        AdministradoraService.listar()
    )


    return render_template(

        "administradoras/listar.html",

        titulo="Gerenciamento de Administradoras",

        administradoras=administradoras,

        novo_url=url_for(
            "administradora.novo"
        ),

        novo_texto="Nova Administradora",

        visualizacao_url=url_for(
            "administradora.completo"
        ),

        exportar_url=url_for(

            "exportacao.exportar_generico",

            modulo="administradora"

        )

    )


@administradora_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
def novo():

    if request.method == "POST":

        nome = request.form.get(
            "nome"
        )

        cliente_proprio = request.form.get(
            "cliente_proprio"
        )


        try:

            administradora = (
                AdministradoraService.criar(

                    nome=nome,

                    cliente_proprio=
                        cliente_proprio

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


            administradora = (
                _administradora_formulario(

                    nome,

                    cliente_proprio

                )
            )


            return render_template(

                "administradoras/form.html",

                titulo="Nova Administradora",

                administradora=administradora,

                origem=None

            )


        flash(

            "Administradora cadastrada com sucesso.",

            "success"

        )


        if administradora.cliente_proprio:

            return redirect(

                url_for(

                    "cliente.novo",

                    id_administradora=
                        administradora.id_administradora,

                    origem="administradora"

                )

            )


        return redirect(

            url_for(
                "administradora.listar"
            )

        )


    return render_template(

        "administradoras/form.html",

        titulo="Nova Administradora",

        administradora=None,

        origem=None

    )


@administradora_bp.route(
    "/<int:id_administradora>/editar",
    methods=["GET", "POST"]
)
def editar(id_administradora):

    administradora = (
        AdministradoraService.buscar_por_id(
            id_administradora
        )
    )

    if request.method == "POST":

        cliente_proprio_anterior = (
            administradora.cliente_proprio
        )

        nome = request.form.get("nome")

        cliente_proprio = request.form.get(
            "cliente_proprio"
        )

        try:

            AdministradoraService.atualizar(

                administradora=administradora,

                nome=nome,

                cliente_proprio=cliente_proprio

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

            administradora.nome = nome or ""

            administradora.cliente_proprio = (
                cliente_proprio == "Sim"
            )

            return render_template(

                "administradoras/form.html",

                titulo="Editar Administradora",

                administradora=administradora,

                origem=request.form.get(
                    "origem"
                )

            )

        flash(
            "Administradora atualizada com sucesso.",
            "success"
        )

        # =================================================
        # FOI ATIVADO COMO CLIENTE PRÓPRIO
        # =================================================

        if (
            not cliente_proprio_anterior
            and administradora.cliente_proprio
        ):

            return redirect(

                url_for(

                    "cliente.novo",

                    id_administradora=(
                        administradora.id_administradora
                    ),

                    origem="administradora"

                )

            )

        # =================================================
        # FLUXO NORMAL
        # =================================================

        origem = request.form.get("origem")

        if origem == "completo":

            return redirect(

                url_for(
                    "administradora.completo"
                )

            )

        return redirect(

            url_for(
                "administradora.listar"
            )

        )

    return render_template(

        "administradoras/form.html",

        titulo="Editar Administradora",

        administradora=administradora,

        origem=request.args.get(
            "origem"
        )

    )


@administradora_bp.route(
    "/<int:id_administradora>/toggle"
)
def toggle(id_administradora):

    administradora = (
        AdministradoraService.buscar_por_id(
            id_administradora
        )
    )


    AdministradoraService.alternar_status(
        administradora
    )


    flash(

        "Status da administradora atualizado.",

        "success"

    )


    if request.args.get(
        "origem"
    ) == "completo":

        return redirect(

            url_for(
                "administradora.completo"
            )

        )


    return redirect(

        url_for(
            "administradora.listar"
        )

    )


@administradora_bp.route(
    "/<int:id_administradora>"
)
def detalhes(id_administradora):

    administradora = (
        AdministradoraService.buscar_por_id(
            id_administradora
        )
    )


    return render_template(

        "administradoras/detalhes.html",

        titulo="Detalhes da Administradora",

        administradora=administradora

    )


@administradora_bp.route(
    "/completo"
)
def completo():

    administradoras = (
        AdministradoraService.listar_completo(
            request.args
        )
    )


    return render_template(

        "administradoras/completo.html",

        titulo="Visualização Completa de Administradoras",

        administradoras=administradoras,

        campos=FILTROS_ADMINISTRADORA,

        campos_filtro=request.args.getlist(
            "campo[]"
        ),

        valores_filtro=request.args.getlist(
            "valor[]"
        )

    )


# =========================================================
# AUXILIAR
# =========================================================

def _administradora_formulario(
    nome,
    cliente_proprio
):

    from app.models import Administradora


    return Administradora(

        nome=nome or "",

        cliente_proprio=(
            cliente_proprio == "Sim"
        )

    )