from datetime import date

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)

from app.services.dashboard_service import (
    DashboardService
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


proteger_blueprint(
    dashboard_bp,
    "Administrador",
    "Operador",
    "Leitor"
)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "usuario_id" not in session:

        return redirect(
            url_for(
                "autenticacao.login"
            )
        )


    # =====================================================
    # DADOS DO ADMINISTRADOR
    # =====================================================

    if session.get("perfil") == "Administrador":

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
                    "dashboard.dashboard"
                )
            )


        if data_inicial > data_final:

            flash(
                "A data inicial não pode ser posterior à data final.",
                "warning"
            )

            return redirect(
                url_for(
                    "dashboard.dashboard"
                )
            )


        comparacao = (
            DashboardService.comparar_periodos(
                data_inicial,
                data_final
            )
        )


        resumo_geral = (
            DashboardService.resumo_geral()
        )


        return render_template(

            "dashboard/index.html",

            data_inicial=data_inicial,

            data_final=data_final,

            atual=comparacao[
                "atual"
            ],

            anterior=comparacao[
                "anterior"
            ],

            percentual_faturamento=comparacao[
                "percentual_faturamento"
            ],

            percentual_atendimentos=comparacao[
                "percentual_atendimentos"
            ],

            periodo_anterior_inicial=comparacao[
                "periodo_anterior_inicial"
            ],

            periodo_anterior_final=comparacao[
                "periodo_anterior_final"
            ],

            resumo_geral=resumo_geral

        )


    # =====================================================
    # OUTROS PERFIS
    # =====================================================

    return render_template(
        "dashboard/index.html"
    )