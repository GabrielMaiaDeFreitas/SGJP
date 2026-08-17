from copy import deepcopy

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.filters.tabela_valores import (
    FILTROS_TABELA_VALORES
)

from app.services.tabela_valores_service import (
    TabelaValoresService
)

from app.services.administradora_service import (
    AdministradoraService
)

from app.services.tipo_servico_service import (
    TipoServicoService
)

from app.exceptions import (
    ValidacaoError
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)


tabela_valores_bp = Blueprint(

    "tabela_valores",

    __name__,

    url_prefix="/tabelas-valores"

)


proteger_blueprint(
    tabela_valores_bp,
    "Administrador"
)


@tabela_valores_bp.route("/")
def listar():

    tabelas = (
        TabelaValoresService.listar()
    )


    return render_template(

        "tabela_valores/listar.html",

        titulo="Gerenciamento de Tabelas de Valores",

        tabelas=tabelas,

        novo_url=url_for(
            "tabela_valores.novo"
        ),

        novo_texto="Nova Tabela",

        visualizacao_url=url_for(
            "tabela_valores.completo"
        ),

        exportar_url=url_for(

            "exportacao.exportar_generico",

            modulo="tabela_valores"

        )

    )


@tabela_valores_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
def novo():

    administradoras = (
        TabelaValoresService
        .administradoras_disponiveis()
    )


    id_administradora = (
        request.args.get(
            "id_administradora",
            type=int
        )
    )


    administradora = None
    tabela = []


    if id_administradora:

        if TabelaValoresService.tabela_existe(
            id_administradora
        ):

            flash(

                "Essa administradora já possui "
                "uma tabela de valores configurada. "
                "Utilize a opção Editar.",

                "warning"

            )

            return redirect(

                url_for(

                    "tabela_valores.editar",

                    id_administradora=(
                        id_administradora
                    )

                )

            )


        administradora, tabela = (
            TabelaValoresService
            .carregar_tabela(
                id_administradora
            )
        )


    if request.method == "POST":

        id_administradora = request.form.get(
            "id_administradora",
            type=int
        )


        if not id_administradora:

            flash(
                "Selecione uma administradora.",
                "warning"
            )

            return render_template(

                "tabela_valores/form.html",

                titulo="Nova Tabela de Valores",

                administradoras=administradoras,

                administradora=None,

                tabela=[]

            )


        if TabelaValoresService.tabela_existe(
            id_administradora
        ):

            flash(

                "Essa administradora já possui "
                "uma tabela de valores configurada. "
                "Utilize a opção Editar.",

                "warning"

            )

            return redirect(

                url_for(

                    "tabela_valores.editar",

                    id_administradora=(
                        id_administradora
                    )

                )

            )


        try:

            dados = (
                TabelaValoresService
                .montar_dados(
                    request.form
                )
            )

            TabelaValoresService.salvar_tabela(

                id_administradora=(
                    id_administradora
                ),

                dados=dados

            )

        except ValidacaoError as erro:

            flash(
                erro.mensagem,
                "warning"
            )

            administradora, tabela = (
                TabelaValoresService
                .carregar_tabela(
                    id_administradora
                )
            )

            return render_template(

                "tabela_valores/form.html",

                titulo="Nova Tabela de Valores",

                administradoras=administradoras,

                administradora=administradora,

                tabela=tabela

            )


        flash(

            "Tabela de valores cadastrada "
            "com sucesso.",

            "success"

        )


        return redirect(

            url_for(
                "tabela_valores.listar"
            )

        )


    return render_template(

        "tabela_valores/form.html",

        titulo="Nova Tabela de Valores",

        administradoras=administradoras,

        administradora=administradora,

        tabela=tabela

    )


@tabela_valores_bp.route(
    "/<int:id_administradora>/editar",
    methods=["GET", "POST"]
)
def editar(id_administradora):

    administradora, tabela = (
        TabelaValoresService
        .carregar_tabela(
            id_administradora
        )
    )


    if request.method == "POST":

        try:

            dados = (
                TabelaValoresService
                .montar_dados(
                    request.form
                )
            )

            TabelaValoresService.salvar_tabela(

                id_administradora=(
                    id_administradora
                ),

                dados=dados

            )

        except ValidacaoError as erro:

            flash(
                erro.mensagem,
                "warning"
            )

            administradora, tabela = (
                TabelaValoresService
                .carregar_tabela(
                    id_administradora
                )
            )

            return render_template(

                "tabela_valores/form.html",

                titulo="Editar Tabela de Valores",

                administradora=administradora,

                tabela=tabela,

                administradoras=[]

            )


        flash(

            "Tabela de valores atualizada "
            "com sucesso.",

            "success"

        )


        return redirect(

            url_for(
                "tabela_valores.listar"
            )

        )


    return render_template(

        "tabela_valores/form.html",

        titulo="Editar Tabela de Valores",

        administradora=administradora,

        tabela=tabela,

        administradoras=[]

    )


@tabela_valores_bp.route(
    "/<int:id_administradora>"
)
def detalhes(id_administradora):

    administradora, tabela = (
        TabelaValoresService
        .detalhes(
            id_administradora
        )
    )


    return render_template(

        "tabela_valores/detalhes.html",

        titulo="Detalhes da Tabela de Valores",

        administradora=administradora,

        tabela=tabela

    )


@tabela_valores_bp.route(
    "/completo"
)
def completo():

    tabelas = (
        TabelaValoresService
        .listar_completo(
            request.args
        )
    )


    campos = deepcopy(
        FILTROS_TABELA_VALORES
    )


    administradoras = (
        AdministradoraService
        .listar_ativas()
    )

    tipos_servico = (
        TipoServicoService
        .listar_ativos()
    )


    for campo in campos:

        if (
            campo["campo"]
            == "fk_administradora_id_administradora"
        ):

            campo["opcoes"] = [

                {
                    "id":
                        administradora.id_administradora,

                    "label":
                        administradora.nome
                }

                for administradora in administradoras

            ]


        elif (
            campo["campo"]
            == "fk_tipo_servico_id_tipo_servico"
        ):

            campo["opcoes"] = [

                {
                    "id":
                        tipo.id_tipo_servico,

                    "label":
                        tipo.nome
                }

                for tipo in tipos_servico

            ]


    return render_template(

        "tabela_valores/completo.html",

        titulo=(
            "Visualização Completa "
            "das Tabelas de Valores"
        ),

        tabelas=tabelas,

        campos=campos,

        campos_filtro=request.args.getlist(
            "campo[]"
        ),

        valores_filtro=request.args.getlist(
            "valor[]"
        )

    )