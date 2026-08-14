from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect
)

from app.exports.config import MODELOS_MAPEADOS
from app.exports.export_service import ExportService
from app.services.filter_service import FilterService

from app.helpers.autorizacao_helper import (proteger_blueprint)

exportacao_bp = Blueprint(

    "exportacao",

    __name__,

    url_prefix="/exportar"

)

proteger_blueprint(exportacao_bp,"Administrador")

@exportacao_bp.route(
    "/<string:modulo>",
    methods=["GET", "POST"]
)
def exportar_generico(modulo):

    mapeamento = MODELOS_MAPEADOS.get(

        modulo

    )

    if not mapeamento:

        flash(

            "Módulo não encontrado para exportação.",

            "error"

        )

        return redirect(

            request.referrer or "/"

        )

    modelo = mapeamento["modelo"]

    filtros_config = mapeamento["filtros_config"]

    colunas = mapeamento["colunas_exportacao"]

    labels = mapeamento["labels"]

    if request.method == "POST":

        colunas_selecionadas = request.form.getlist(

            "colunas"

        )

        if not colunas_selecionadas:

            flash(

                "Selecione pelo menos uma coluna.",

                "warning"

            )

            return redirect(

                request.url

            )

        formatos = request.form.getlist(

            "formatos"

        )

        if not formatos:

            flash(

                "Selecione pelo menos um formato para exportação.",

                "warning"

            )

            return redirect(

                request.url

            )

        ordem_final = (

            request.values.get(

                "ordenar_por"

            )

            or

            request.values.get(

                "sort"

            )

            or

            mapeamento["ordenar_por"]

        )

        if "listar_service" in mapeamento:

            try:

                dados = mapeamento["listar_service"](

                    request.values

                )

            except TypeError:

                dados = mapeamento["listar_service"]()

        else:

            dados = FilterService.listar(

                modelo=modelo,

                filtros=request.values,

                configuracoes=filtros_config,

                ordenar_por=ordem_final

            )

        return ExportService.exportar(

            dados=dados,

            colunas=colunas_selecionadas,

            formatos=formatos,

            nome_arquivo=modulo,

            titulo=mapeamento["titulo"],

            labels=labels

        )

    return render_template(

        "exportacao/selecionar_colunas.html",

        modulo=modulo,

        titulo=f"Exportar {mapeamento['titulo']}",

        colunas=colunas,

        labels=labels

    )