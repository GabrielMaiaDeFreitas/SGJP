from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.constants.motorista import (
    CATEGORIAS_CNH
)

from app.filters.motorista import (
    FILTROS_MOTORISTA
)

from app.services.motorista_service import (
    MotoristaService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)


motorista_bp = Blueprint(
    "motorista",
    __name__,
    url_prefix="/motoristas"
)


proteger_blueprint(
    motorista_bp,
    "Administrador"
)


@motorista_bp.route("/")
def listar():

    motoristas = MotoristaService.listar()

    return render_template(

        "motoristas/listar.html",

        motoristas=motoristas,

        titulo="Gerenciamento de Motoristas"

    )


@motorista_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
def novo():

    if request.method == "POST":

        dados = _dados_formulario()


        try:

            MotoristaService.criar(
                **dados
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

            motorista = _motorista_formulario(
                dados
            )

            return render_template(

                "motoristas/form.html",

                titulo="Novo Motorista",

                motorista=motorista,

                categorias=CATEGORIAS_CNH

            )


        flash(
            "Motorista cadastrado com sucesso.",
            "success"
        )

        return redirect(
            url_for(
                "motorista.listar"
            )
        )


    return render_template(

        "motoristas/form.html",

        titulo="Novo Motorista",

        motorista=None,

        categorias=CATEGORIAS_CNH

    )


@motorista_bp.route(
    "/<int:id_motorista>"
)
def detalhes(id_motorista):

    motorista = MotoristaService.buscar_por_id(
        id_motorista
    )

    return render_template(

        "motoristas/detalhes.html",

        motorista=motorista,

        titulo="Detalhes do Motorista"

    )


@motorista_bp.route(
    "/<int:id_motorista>/editar",
    methods=["GET", "POST"]
)
def editar(id_motorista):

    motorista = MotoristaService.buscar_por_id(
        id_motorista
    )


    if request.method == "POST":

        dados = _dados_formulario()


        try:

            MotoristaService.atualizar(

                motorista=motorista,

                **dados

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

            motorista_formulario = (
                _motorista_formulario(
                    dados
                )
            )

            return render_template(

                "motoristas/form.html",

                titulo="Editar Motorista",

                motorista=motorista_formulario,

                origem=request.form.get(
                    "origem"
                ),

                categorias=CATEGORIAS_CNH

            )


        flash(
            "Motorista atualizado com sucesso.",
            "success"
        )


        origem = request.form.get(
            "origem"
        )


        if origem == "completo":

            return redirect(
                url_for(
                    "motorista.completo"
                )
            )


        return redirect(
            url_for(
                "motorista.listar"
            )
        )


    return render_template(

        "motoristas/form.html",

        titulo="Editar Motorista",

        motorista=motorista,

        origem=request.args.get(
            "origem"
        ),

        categorias=CATEGORIAS_CNH

    )


@motorista_bp.route(
    "/<int:id_motorista>/toggle"
)
def toggle(id_motorista):

    motorista = MotoristaService.buscar_por_id(
        id_motorista
    )

    MotoristaService.alternar_status(
        motorista
    )


    flash(
        "Status do motorista atualizado.",
        "success"
    )


    if request.args.get(
        "origem"
    ) == "completo":

        return redirect(
            url_for(
                "motorista.completo"
            )
        )


    return redirect(
        url_for(
            "motorista.listar"
        )
    )


@motorista_bp.route(
    "/completo"
)
def completo():

    motoristas = (
        MotoristaService.listar_completo(
            request.args
        )
    )


    campos_filtro = (
        request.args.getlist(
            "campo[]"
        )
    )


    valores_filtro = (
        request.args.getlist(
            "valor[]"
        )
    )


    return render_template(

        "motoristas/completo.html",

        titulo="Visualização Completa de Motoristas",

        motoristas=motoristas,

        campos=FILTROS_MOTORISTA,

        campos_filtro=campos_filtro,

        valores_filtro=valores_filtro

    )


# =========================================================
# FUNÇÕES AUXILIARES DA ROUTE
# =========================================================

def _dados_formulario():

    return {

        "matricula":
            request.form.get(
                "matricula"
            ),

        "nome":
            request.form.get(
                "nome"
            ),

        "numero_cnh":
            request.form.get(
                "numero_cnh"
            ),

        "categoria_cnh":
            request.form.get(
                "categoria_cnh"
            ),

        "validade_cnh":
            request.form.get(
                "validade_cnh"
            ),

        "validade_toxicologico":
            request.form.get(
                "validade_toxicologico"
            )

    }


def _motorista_formulario(
    dados
):

    from app.models import Motorista
    from datetime import datetime


    motorista = Motorista(

        matricula=dados["matricula"] or "",

        nome=dados["nome"] or "",

        numero_cnh=dados["numero_cnh"] or "",

        categoria_cnh=dados["categoria_cnh"] or ""

    )


    if dados["validade_cnh"]:

        try:

            motorista.validade_cnh = (
                datetime.strptime(
                    dados["validade_cnh"],
                    "%Y-%m-%d"
                ).date()
            )

        except ValueError:

            motorista.validade_cnh = None


    if dados["validade_toxicologico"]:

        try:

            motorista.validade_toxicologico = (
                datetime.strptime(
                    dados["validade_toxicologico"],
                    "%Y-%m-%d"
                ).date()
            )

        except ValueError:

            motorista.validade_toxicologico = None


    return motorista