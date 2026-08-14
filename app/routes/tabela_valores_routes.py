from decimal import Decimal
from copy import deepcopy


from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

from app.models import (Administradora, TipoServico, TabelaValores)

from app.services.tabela_valores_service import (
    TabelaValoresService
)

from app.filters.tabela_valores import (
    FILTROS_TABELA_VALORES
)

from app.helpers.autorizacao_helper import (proteger_blueprint)

from copy import deepcopy


tabela_valores_bp = Blueprint(

    "tabela_valores",

    __name__,

    url_prefix="/tabelas-valores"

)

proteger_blueprint(tabela_valores_bp,"Administrador")

@tabela_valores_bp.route("/")
def listar():

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    tabelas = TabelaValoresService.listar(
        request.args
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


@tabela_valores_bp.route("/novo",methods=["GET", "POST"])
def novo():

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    administradoras = (

        TabelaValoresService.administradoras_disponiveis()

    )

    id_administradora = request.args.get(

        "id_administradora",

        type=int

    )

    administradora = None

    tabela = []

    if id_administradora:

        if TabelaValoresService.tabela_existe(

            id_administradora

        ):

            flash(

                "Essa administradora já possui uma tabela de valores cadastrada. Utilize a opção Editar.",

                "warning"

            )

            return redirect(

                url_for(

                    "tabela_valores.editar",

                    id_administradora=id_administradora

                )

            )

        administradora, tabela = (

            TabelaValoresService.carregar_tabela(

                id_administradora

            )

        )

    if request.method == "POST":

        id_administradora = int(

            request.form[
                "id_administradora"
            ]

        )

        if TabelaValoresService.tabela_existe(

            id_administradora

        ):

            flash(

                "Essa administradora já possui uma tabela de valores cadastrada. Utilize a opção Editar.",

                "warning"

            )

            return redirect(

                url_for(

                    "tabela_valores.editar",

                    id_administradora=id_administradora

                )

            )

        dados = TabelaValoresService.montar_dados(

            request.form

        )

        TabelaValoresService.salvar_tabela(

            id_administradora=id_administradora,

            dados=dados

        )

        flash(

            "Tabela de valores cadastrada com sucesso.",

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

@tabela_valores_bp.route("/<int:id_administradora>/editar", methods=["GET", "POST"])
def editar(id_administradora):

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    administradora, tabela = (

        TabelaValoresService.carregar_tabela(
            id_administradora
        )

    )

    if request.method == "POST":

        dados = TabelaValoresService.montar_dados(

            request.form

        )

        TabelaValoresService.salvar_tabela(

            id_administradora=id_administradora,

            dados=dados

        )

        flash(

            "Tabela de valores atualizada com sucesso.",

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

@tabela_valores_bp.route("/<int:id_administradora>")
def detalhes(id_administradora):

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    administradora, tabela = (

        TabelaValoresService.detalhes(
            id_administradora
        )

    )

    return render_template(

        "tabela_valores/detalhes.html",

        titulo="Detalhes da Tabela de Valores",

        administradora=administradora,

        tabela=tabela

    )


@tabela_valores_bp.route("/completo")
def completo():

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    tabelas = TabelaValoresService.listar_completo(

        request.args

    )

    campos = deepcopy(
        FILTROS_TABELA_VALORES
    )

    administradoras = Administradora.query.filter_by(

        ativo=True

    ).order_by(

        Administradora.nome

    ).all()

    tipos_servico = TipoServico.query.filter_by(

        ativo=True

    ).order_by(

        TipoServico.nome

    ).all()

    for campo in campos:

        if campo["campo"] == "fk_administradora_id_administradora":

            campo["opcoes"] = [

                {

                    "id": administradora.id_administradora,

                    "label": administradora.nome

                }

                for administradora in administradoras

            ]

        elif campo["campo"] == "fk_tipo_servico_id_tipo_servico":

            campo["opcoes"] = [

                {

                    "id": tipo.id_tipo_servico,

                    "label": tipo.nome

                }

                for tipo in tipos_servico

            ]

    return render_template(

        "tabela_valores/completo.html",

        titulo="Visualização Completa das Tabelas de Valores",

        tabelas=tabelas,

        campos=campos,

        campos_filtro=request.args.getlist(
            "campo[]"
        ),

        valores_filtro=request.args.getlist(
            "valor[]"
        )

    )