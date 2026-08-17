from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)


from app.filters.caminhao import (
    FILTROS_CAMINHAO
)

from app.services.caminhao_service import (
    CaminhaoService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)


caminhao_bp = Blueprint(

    "caminhao",

    __name__,

    url_prefix="/caminhoes"

)


proteger_blueprint(
    caminhao_bp,
    "Administrador"
)


@caminhao_bp.route("/")
def listar():

    caminhoes = CaminhaoService.listar()

    return render_template(

        "caminhoes/listar.html",

        titulo="Gerenciamento de Caminhões",

        caminhoes=caminhoes,

        novo_url=url_for(
            "caminhao.novo"
        ),

        novo_texto="Novo Caminhão",

        visualizacao_url=url_for(
            "caminhao.completo"
        ),

        exportar_url=url_for(
            "exportacao.exportar_generico",
            modulo="caminhao"
        )

    )


@caminhao_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
def novo():

    if request.method == "POST":

        placa = request.form.get(
            "placa"
        )

        modelo = request.form.get(
            "modelo"
        )


        try:

            CaminhaoService.criar(

                placa=placa,

                modelo=modelo

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


            caminhao = _caminhao_formulario(

                placa,

                modelo

            )


            return render_template(

                "caminhoes/form.html",

                titulo="Novo Caminhão",

                caminhao=caminhao,

                origem=None

            )


        flash(

            "Caminhão cadastrado com sucesso.",

            "success"

        )


        return redirect(

            url_for(
                "caminhao.listar"
            )

        )


    return render_template(

        "caminhoes/form.html",

        titulo="Novo Caminhão",

        caminhao=None,

        origem=None

    )


@caminhao_bp.route(
    "/<int:id_caminhao>/editar",
    methods=["GET", "POST"]
)
def editar(id_caminhao):

    caminhao = CaminhaoService.buscar_por_id(
        id_caminhao
    )


    if request.method == "POST":

        placa = request.form.get(
            "placa"
        )

        modelo = request.form.get(
            "modelo"
        )


        try:

            CaminhaoService.atualizar(

                caminhao=caminhao,

                placa=placa,

                modelo=modelo

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


            caminhao.placa = (
                placa or ""
            )

            caminhao.modelo = (
                modelo or ""
            )


            return render_template(

                "caminhoes/form.html",

                titulo="Editar Caminhão",

                caminhao=caminhao,

                origem=request.form.get(
                    "origem"
                )

            )


        flash(

            "Caminhão atualizado com sucesso.",

            "success"

        )


        origem = request.form.get(
            "origem"
        )


        if origem == "completo":

            return redirect(

                url_for(
                    "caminhao.completo"
                )

            )


        return redirect(

            url_for(
                "caminhao.listar"
            )

        )


    return render_template(

        "caminhoes/form.html",

        titulo="Editar Caminhão",

        caminhao=caminhao,

        origem=request.args.get(
            "origem"
        )

    )


@caminhao_bp.route(
    "/<int:id_caminhao>/toggle"
)
def toggle(id_caminhao):

    caminhao = CaminhaoService.buscar_por_id(
        id_caminhao
    )


    CaminhaoService.alternar_status(
        caminhao
    )


    flash(

        "Status do caminhão atualizado.",

        "success"

    )


    if request.args.get(
        "origem"
    ) == "completo":

        return redirect(

            url_for(
                "caminhao.completo"
            )

        )


    return redirect(

        url_for(
            "caminhao.listar"
        )

    )


@caminhao_bp.route(
    "/<int:id_caminhao>"
)
def detalhes(id_caminhao):

    caminhao = CaminhaoService.buscar_por_id(
        id_caminhao
    )


    return render_template(

        "caminhoes/detalhes.html",

        titulo="Detalhes do Caminhão",

        caminhao=caminhao

    )


@caminhao_bp.route(
    "/completo"
)
def completo():

    caminhoes = (
        CaminhaoService.listar_completo(
            request.args
        )
    )


    return render_template(

        "caminhoes/completo.html",

        titulo="Visualização Completa de Caminhões",

        caminhoes=caminhoes,

        campos=FILTROS_CAMINHAO,

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

def _caminhao_formulario(
    placa,
    modelo
):

    from app.models import Caminhao

    return Caminhao(

        placa=placa or "",

        modelo=modelo or ""

    )