from datetime import date

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    flash
)

from app.models import Motorista

from app.services.relatorios.motoristas_service import (
    MotoristasRelatorioService
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)

motoristas_relatorio_bp = Blueprint(
    "relatorio_motoristas",
    __name__,
    url_prefix="/relatorios/motoristas"
)
proteger_blueprint(
    motoristas_relatorio_bp,
    "Administrador",
    "Operador",
    "Leitor"
)

@motoristas_relatorio_bp.route("/")
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
                "relatorio_motoristas.listar"
            )
        )

    if data_inicial > data_final:

        flash(
            "A data inicial não pode ser posterior à data final.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_motoristas.listar"
            )
        )

    relatorio = (
        MotoristasRelatorioService.gerar_relatorio(
            data_inicial,
            data_final
        )
    )

    return render_template(
        "relatorios/motoristas/motoristas.html",

        motoristas=relatorio["motoristas"],

        faturamento_total=relatorio[
            "faturamento_total"
        ],

        quantidade_atendimentos_total=relatorio[
            "quantidade_atendimentos_total"
        ],

        km_total=relatorio[
            "km_total"
        ],

        valor_comissao_total=relatorio[
            "valor_comissao_total"
        ],

        data_inicial=data_inicial,

        data_final=data_final
    )


@motoristas_relatorio_bp.route(
    "/<int:id_motorista>"
)
def detalhes(id_motorista):

    data_inicial_texto = request.args.get(
        "data_inicial"
    )

    data_final_texto = request.args.get(
        "data_final"
    )

    if not data_inicial_texto or not data_final_texto:

        return redirect(
            url_for(
                "relatorio_motoristas.listar"
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
                "relatorio_motoristas.listar"
            )
        )

    if data_inicial > data_final:

        flash(
            "A data inicial não pode ser posterior à data final.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_motoristas.listar"
            )
        )

    motorista = Motorista.query.get_or_404(
        id_motorista
    )

    atendimentos = (
        MotoristasRelatorioService.buscar_detalhes(
            id_motorista,
            data_inicial,
            data_final
        )
    )

    return render_template(
        "relatorios/motoristas/detalhes.html",

        titulo="Atendimentos do Motorista",

        motorista=motorista,

        atendimentos=atendimentos,

        data_inicial=data_inicial,

        data_final=data_final
    )