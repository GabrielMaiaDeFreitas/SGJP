from datetime import date

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    flash
)

from app.models import Caminhao

from app.services.relatorios.caminhoes_service import (
    CaminhoesRelatorioService
)
from app.helpers.autorizacao_helper import (
    proteger_blueprint
)


caminhoes_relatorio_bp = Blueprint(
    "relatorio_caminhoes",
    __name__,
    url_prefix="/relatorios/caminhoes"
)

proteger_blueprint(
    caminhoes_relatorio_bp,
    "Administrador",
    "Operador",
    "Leitor"
)


@caminhoes_relatorio_bp.route("/")
def listar():

    hoje = date.today()

    data_inicial_texto = request.args.get(
        "data_inicial",
        f"{hoje.year:04d}-{hoje.month:02d}-01"
    )

    data_final_texto = request.args.get(
        "data_final",
        hoje.isoformat()
    )

    try:

        data_inicial = date.fromisoformat(
            data_inicial_texto
        )

        data_final = date.fromisoformat(
            data_final_texto
        )

    except ValueError:

        flash(
            "Período de datas inválido.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_caminhoes.listar"
            )
        )

    if data_inicial > data_final:

        flash(
            "A data inicial não pode ser posterior à data final.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_caminhoes.listar"
            )
        )

    relatorio = CaminhoesRelatorioService.gerar_relatorio(
        data_inicial,
        data_final
    )

    return render_template(
        "relatorios/caminhoes/caminhoes.html",

        caminhoes=relatorio["caminhoes"],

        faturamento_total=relatorio[
            "faturamento_total"
        ],

        quantidade_atendimentos_total=relatorio[
            "quantidade_atendimentos_total"
        ],

        km_total=relatorio[
            "km_total"
        ],

        data_inicial=data_inicial,

        data_final=data_final
    )


@caminhoes_relatorio_bp.route(
    "/<int:id_caminhao>"
)
def detalhes(id_caminhao):

    data_inicial_texto = request.args.get(
        "data_inicial"
    )

    data_final_texto = request.args.get(
        "data_final"
    )

    if not data_inicial_texto or not data_final_texto:

        return redirect(
            url_for(
                "relatorio_caminhoes.listar"
            )
        )

    try:

        data_inicial = date.fromisoformat(
            data_inicial_texto
        )

        data_final = date.fromisoformat(
            data_final_texto
        )

    except ValueError:

        flash(
            "Período de datas inválido.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_caminhoes.listar"
            )
        )

    if data_inicial > data_final:

        flash(
            "A data inicial não pode ser posterior à data final.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_caminhoes.listar"
            )
        )

    caminhao = Caminhao.query.get_or_404(
        id_caminhao
    )

    atendimentos = (
        CaminhoesRelatorioService.buscar_detalhes(
            id_caminhao,
            data_inicial,
            data_final
        )
    )

    return render_template(
        "relatorios/caminhoes/detalhes.html",

        titulo="Atendimentos do Caminhão",

        caminhao=caminhao,

        atendimentos=atendimentos,

        data_inicial=data_inicial,

        data_final=data_final
    )