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
from app.helpers.autorizacao_helper import (
    requer_perfil,
    proteger_blueprint
)



parceiros_relatorio_bp = Blueprint(
    "relatorio_parceiros",
    __name__,
    url_prefix="/relatorios/parceiros"
)

proteger_blueprint(
    parceiros_relatorio_bp,
    "Administrador",
    "Operador",
    "Leitor"
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
    "/<int:id_administradora>"
)
def detalhes(id_administradora):

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

    administradora, atendimentos = (
        ParceirosRelatorioService.buscar_detalhes(
            id_administradora,
            data_inicial,
            data_final
        )
    )

    return render_template(

        "relatorios/parceiros/parceiros_detalhes.html",

        titulo="Atendimentos do Parceiro",

        administradora=administradora,

        atendimentos=atendimentos,

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

@parceiros_relatorio_bp.route(
    "/<int:id_administradora>/clientes/<int:id_cliente>"
)
def clientes_detalhes(
    id_administradora,
    id_cliente
):

    data_inicial_texto = request.args.get(
        "data_inicial"
    )

    data_final_texto = request.args.get(
        "data_final"
    )

    if not data_inicial_texto or not data_final_texto:

        return redirect(
            url_for(
                "relatorio_parceiros.clientes",
                id_administradora=id_administradora
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
                "relatorio_parceiros.clientes",
                id_administradora=id_administradora
            )
        )

    if data_inicial > data_final:

        flash(
            "A data inicial não pode ser posterior à data final.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_parceiros.clientes",
                id_administradora=id_administradora
            )
        )

    administradora, cliente, atendimentos = (
        ParceirosRelatorioService.buscar_detalhes_cliente(
            id_administradora,
            id_cliente,
            data_inicial,
            data_final
        )
    )

    return render_template(
        "relatorios/parceiros/clientes_detalhes.html",

        titulo="Atendimentos do Cliente",

        administradora=administradora,

        cliente=cliente,

        atendimentos=atendimentos,

        data_inicial=data_inicial,

        data_final=data_final
    )

@parceiros_relatorio_bp.route(
    "/<int:id_administradora>/clientes/<int:id_cliente>/fechamento"
)
@requer_perfil("Administrador")
def fechamento(
    id_administradora,
    id_cliente
):

    data_inicial_texto = request.args.get(
        "data_inicial"
    )

    data_final_texto = request.args.get(
        "data_final"
    )

    if not data_inicial_texto or not data_final_texto:

        return redirect(
            url_for(
                "relatorio_parceiros.clientes",
                id_administradora=id_administradora
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
                "relatorio_parceiros.clientes",
                id_administradora=id_administradora,
                data_inicial=data_inicial_texto,
                data_final=data_final_texto
            )
        )

    if data_inicial > data_final:

        flash(
            "A data inicial não pode ser posterior à data final.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_parceiros.clientes",
                id_administradora=id_administradora,
                data_inicial=data_inicial.isoformat(),
                data_final=data_final.isoformat()
            )
        )

    (
        administradora,
        cliente,
        atendimentos
    ) = ParceirosRelatorioService.buscar_atendimentos_para_fechamento(

        id_administradora,

        id_cliente,

        data_inicial,

        data_final

    )

    return render_template(

        "relatorios/parceiros/completo_fechamento.html",

        titulo="Fechamento de Pagamento",

        administradora=administradora,

        cliente=cliente,

        atendimentos=atendimentos,

        data_inicial=data_inicial,

        data_final=data_final

    )

@parceiros_relatorio_bp.route(
    "/<int:id_administradora>/clientes/<int:id_cliente>/fechamento",
    methods=["POST"]
)
@requer_perfil("Administrador")
def realizar_fechamento(
    id_administradora,
    id_cliente
):

    data_inicial_texto = request.form.get(
        "data_inicial"
    )

    data_final_texto = request.form.get(
        "data_final"
    )

    if not data_inicial_texto or not data_final_texto:

        flash(
            "Período do fechamento não informado.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_parceiros.clientes_detalhes",
                id_administradora=id_administradora,
                id_cliente=id_cliente
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
                "relatorio_parceiros.clientes_detalhes",
                id_administradora=id_administradora,
                id_cliente=id_cliente,
                data_inicial=data_inicial_texto,
                data_final=data_final_texto
            )
        )

    if data_inicial > data_final:

        flash(
            "A data inicial não pode ser posterior à data final.",
            "warning"
        )

        return redirect(
            url_for(
                "relatorio_parceiros.clientes_detalhes",
                id_administradora=id_administradora,
                id_cliente=id_cliente,
                data_inicial=data_inicial.isoformat(),
                data_final=data_final.isoformat()
            )
        )

    quantidade = (
        ParceirosRelatorioService.realizar_fechamento(

            id_administradora,

            id_cliente,

            data_inicial,

            data_final

        )
    )

    if quantidade == 0:

        flash(
            "Nenhum atendimento aguardando fechamento foi encontrado.",
            "warning"
        )

    else:

        flash(
            f"{quantidade} atendimento(s) foram quitados com sucesso.",
            "success"
        )

    return redirect(
        url_for(
            "relatorio_parceiros.clientes_detalhes",
            id_administradora=id_administradora,
            id_cliente=id_cliente,
            data_inicial=data_inicial.isoformat(),
            data_final=data_final.isoformat()
        )
    )