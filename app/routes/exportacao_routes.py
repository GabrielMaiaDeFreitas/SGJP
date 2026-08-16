from datetime import date

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect
)

from app.models import (
    Caminhao,
    Motorista
)

from app.exports.config import (
    MODELOS_MAPEADOS
)

from app.exports.export_service import (
    ExportService
)

from app.services.filter_service import (
    FilterService
)

from app.services.relatorios.caminhoes_service import (
    CaminhoesRelatorioService
)

from app.services.relatorios.motoristas_service import (
    MotoristasRelatorioService
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)


exportacao_bp = Blueprint(

    "exportacao",

    __name__,

    url_prefix="/exportar"

)


proteger_blueprint(
    exportacao_bp,
    "Administrador"
)


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

    filtros_config = mapeamento[
        "filtros_config"
    ]

    colunas = mapeamento[
        "colunas_exportacao"
    ]

    labels = mapeamento[
        "labels"
    ]

    titulo_exportacao = (
        f"Exportar {mapeamento['titulo']}"
    )


    # =====================================================
    # TÍTULO DA EXPORTAÇÃO
    # =====================================================

    if modulo == "relatorio_caminhao_detalhes":

        id_caminhao = request.values.get(
            "id_caminhao",
            type=int
        )

        if id_caminhao:

            caminhao = Caminhao.query.get(
                id_caminhao
            )

            if caminhao:

                titulo_exportacao = (

                    f"Atendimentos do Caminhão "

                    f"{caminhao.modelo} - "
                    f"{caminhao.placa}"

                )


    elif modulo == "relatorio_motorista_detalhes":

        id_motorista = request.values.get(
            "id_motorista",
            type=int
        )

        if id_motorista:

            motorista = Motorista.query.get(
                id_motorista
            )

            if motorista:

                titulo_exportacao = (

                    f"Atendimentos do Motorista "

                    f"{motorista.nome}"

                )


    # =====================================================
    # PROCESSAMENTO DA EXPORTAÇÃO
    # =====================================================

    if request.method == "POST":

        colunas_selecionadas = (
            request.form.getlist(
                "colunas"
            )
        )

        if not colunas_selecionadas:

            flash(
                "Selecione pelo menos uma coluna.",
                "warning"
            )

            return redirect(
                request.url
            )


        formatos = (
            request.form.getlist(
                "formatos"
            )
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

            mapeamento[
                "ordenar_por"
            ]

        )


        # =================================================
        # DETALHES DO CAMINHÃO
        # =================================================

        if modulo == "relatorio_caminhao_detalhes":

            id_caminhao = request.values.get(
                "id_caminhao",
                type=int
            )

            data_inicial = request.values.get(
                "data_inicial"
            )

            data_final = request.values.get(
                "data_final"
            )

            if (
                not id_caminhao
                or not data_inicial
                or not data_final
            ):

                flash(
                    "Dados do relatório do caminhão não foram informados.",
                    "warning"
                )

                return redirect(
                    request.referrer or "/"
                )


            try:

                data_inicial = date.fromisoformat(
                    data_inicial
                )

                data_final = date.fromisoformat(
                    data_final
                )

            except ValueError:

                flash(
                    "Período de datas inválido.",
                    "warning"
                )

                return redirect(
                    request.referrer or "/"
                )


            dados = (
                CaminhoesRelatorioService.buscar_detalhes(

                    id_caminhao,

                    data_inicial,

                    data_final

                )
            )


        # =================================================
        # DETALHES DO MOTORISTA
        # =================================================

        elif modulo == "relatorio_motorista_detalhes":

            id_motorista = request.values.get(
                "id_motorista",
                type=int
            )

            data_inicial = request.values.get(
                "data_inicial"
            )

            data_final = request.values.get(
                "data_final"
            )

            if (
                not id_motorista
                or not data_inicial
                or not data_final
            ):

                flash(
                    "Dados do relatório do motorista não foram informados.",
                    "warning"
                )

                return redirect(
                    request.referrer or "/"
                )


            try:

                data_inicial = date.fromisoformat(
                    data_inicial
                )

                data_final = date.fromisoformat(
                    data_final
                )

            except ValueError:

                flash(
                    "Período de datas inválido.",
                    "warning"
                )

                return redirect(
                    request.referrer or "/"
                )


            dados = (
                MotoristasRelatorioService.buscar_detalhes(

                    id_motorista,

                    data_inicial,

                    data_final

                )
            )


        # =================================================
        # RELATÓRIOS QUE POSSUEM SERVICE PRÓPRIO
        # =================================================

        elif "listar_service" in mapeamento:

            try:

                dados = mapeamento[
                    "listar_service"
                ](
                    request.values
                )

            except TypeError:

                dados = mapeamento[
                    "listar_service"
                ]()


            # O relatório de motoristas retorna
            # um dicionário contendo o relatório
            # e o resumo do período.
            #
            # A exportação precisa somente da
            # lista de motoristas.

            if modulo == "relatorio_motoristas":

                if isinstance(
                    dados,
                    dict
                ):

                    dados = dados.get(
                        "motoristas",
                        []
                    )


        # =================================================
        # EXPORTAÇÕES NORMAIS
        # =================================================

        else:

            dados = FilterService.listar(

                modelo=modelo,

                filtros=request.values,

                configuracoes=filtros_config,

                ordenar_por=ordem_final

            )


        # =================================================
        # GERAR ARQUIVO
        # =================================================

        return ExportService.exportar(

            dados=dados,

            colunas=colunas_selecionadas,

            formatos=formatos,

            nome_arquivo=modulo,

            titulo=mapeamento[
                "titulo"
            ],

            labels=labels

        )


    # =====================================================
    # TELA DE SELEÇÃO DE COLUNAS
    # =====================================================

    return render_template(

        "exportacao/selecionar_colunas.html",

        modulo=modulo,

        titulo=titulo_exportacao,

        colunas=colunas,

        labels=labels

    )