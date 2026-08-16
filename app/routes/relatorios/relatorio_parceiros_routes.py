from datetime import date

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    flash
)

from app.services.relatorios.parceiros_service import (
    ParceirosRelatorioService
)


parceiros_relatorio_bp = Blueprint(
    "relatorio_parceiros",
    __name__,
    url_prefix="/relatorios/parceiros"
)


@parceiros_relatorio_bp.route("/")
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
                "relatorio_parceiros.listar"
            )
        )

    if data_inicial > data_final:

        flash(
            "A data inicial não pode ser posterior à data final.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_parceiros.listar"
            )
        )

    resultado = (
        ParceirosRelatorioService.gerar_relatorio(
            data_inicial,
            data_final
        )
    )

    return render_template(

        "relatorios/parceiros/parceiros.html",

        parceiros=resultado["parceiros"],

        faturamento_total=resultado[
            "faturamento_total"
        ],

        km_total=resultado[
            "km_total"
        ],

        quantidade_atendimentos_total=resultado[
            "quantidade_atendimentos_total"
        ],

        valor_medio_por_km_total=resultado[
            "valor_medio_por_km_total"
        ],

        data_inicial=data_inicial,

        data_final=data_final

    )


@parceiros_relatorio_bp.route(
    "/<int:id_administradora>/clientes"
)
def clientes(id_administradora):

    data_inicial_texto = request.args.get(
        "data_inicial"
    )

    data_final_texto = request.args.get(
        "data_final"
    )

    if not data_inicial_texto or not data_final_texto:

        return redirect(
            url_for(
                "relatorio_parceiros.listar"
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
                "relatorio_parceiros.listar"
            )
        )

    if data_inicial > data_final:

        flash(
            "A data inicial não pode ser posterior à data final.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_parceiros.listar"
            )
        )

    resultado = (
        ParceirosRelatorioService.gerar_relatorio_por_cliente(

            id_administradora,

            data_inicial,

            data_final

        )
    )

    return render_template(

        "relatorios/parceiros/clientes.html",

        administradora=resultado[
            "administradora"
        ],

        clientes=resultado[
            "clientes"
        ],

        faturamento_total=resultado[
            "faturamento_total"
        ],

        km_total=resultado[
            "km_total"
        ],

        quantidade_atendimentos_total=resultado[
            "quantidade_atendimentos_total"
        ],

        valor_medio_por_km_total=resultado[
            "valor_medio_por_km_total"
        ],

        data_inicial=data_inicial,

        data_final=data_final

    )