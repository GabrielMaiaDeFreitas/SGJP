from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.filters.tipo_servico import (
    FILTROS_TIPO_SERVICO
)

from app.services.tipo_servico_service import (
    TipoServicoService
)

from app.exceptions import (
    CampoObrigatorioError,
    RecursoDuplicadoError,
    ValidacaoError
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)


tipo_servico_bp = Blueprint(
    "tipo_servico",
    __name__,
    url_prefix="/tipos-servico"
)


proteger_blueprint(
    tipo_servico_bp,
    "Administrador"
)


@tipo_servico_bp.route("/")
def listar():

    tipos_servico = (
        TipoServicoService.listar()
    )


    return render_template(

        "tipos_servico/listar.html",

        titulo="Gerenciamento de Tipos de Serviço",

        tipos_servico=tipos_servico,

        novo_url=url_for(
            "tipo_servico.novo"
        ),

        novo_texto="Novo Tipo de Serviço",

        visualizacao_url=url_for(
            "tipo_servico.completo"
        ),

        exportar_url=url_for(

            "exportacao.exportar_generico",

            modulo="tipo_servico"

        )

    )


@tipo_servico_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
def novo():

    if request.method == "POST":

        nome = request.form.get(
            "nome"
        )


        try:

            TipoServicoService.criar(
                nome
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


            tipo_servico = _tipo_servico_formulario(
                nome
            )


            return render_template(

                "tipos_servico/form.html",

                titulo="Novo Tipo de Serviço",

                tipo_servico=tipo_servico

            )


        flash(

            "Tipo de serviço cadastrado "
            "com sucesso.",

            "success"

        )


        return redirect(

            url_for(
                "tipo_servico.listar"
            )

        )


    return render_template(

        "tipos_servico/form.html",

        titulo="Novo Tipo de Serviço",

        tipo_servico=None

    )


@tipo_servico_bp.route(
    "/<int:id_tipo_servico>/editar",
    methods=["GET", "POST"]
)
def editar(id_tipo_servico):

    tipo_servico = (
        TipoServicoService.buscar_por_id(
            id_tipo_servico
        )
    )


    if request.method == "POST":

        nome = request.form.get(
            "nome"
        )


        try:

            TipoServicoService.atualizar(

                tipo_servico=tipo_servico,

                nome=nome

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


            tipo_servico.nome = (
                nome or ""
            )


            return render_template(

                "tipos_servico/form.html",

                titulo="Editar Tipo de Serviço",

                tipo_servico=tipo_servico,

                origem=request.form.get(
                    "origem"
                )

            )


        flash(

            "Tipo de serviço atualizado "
            "com sucesso.",

            "success"

        )


        if request.form.get(
            "origem"
        ) == "completo":

            return redirect(

                url_for(
                    "tipo_servico.completo"
                )

            )


        return redirect(

            url_for(
                "tipo_servico.listar"
            )

        )


    return render_template(

        "tipos_servico/form.html",

        titulo="Editar Tipo de Serviço",

        tipo_servico=tipo_servico,

        origem=request.args.get(
            "origem"
        )

    )


@tipo_servico_bp.route(
    "/<int:id_tipo_servico>/toggle"
)
def toggle(id_tipo_servico):

    tipo_servico = (
        TipoServicoService.buscar_por_id(
            id_tipo_servico
        )
    )


    TipoServicoService.alternar_status(
        tipo_servico
    )


    flash(

        "Status atualizado com sucesso.",

        "success"

    )


    if request.args.get(
        "origem"
    ) == "completo":

        return redirect(

            url_for(
                "tipo_servico.completo"
            )

        )


    return redirect(

        url_for(
            "tipo_servico.listar"
        )

    )


@tipo_servico_bp.route(
    "/<int:id_tipo_servico>"
)
def detalhes(id_tipo_servico):

    tipo_servico = (
        TipoServicoService.buscar_por_id(
            id_tipo_servico
        )
    )


    return render_template(

        "tipos_servico/detalhes.html",

        titulo="Detalhes do Tipo de Serviço",

        tipo_servico=tipo_servico

    )


@tipo_servico_bp.route(
    "/completo"
)
def completo():

    tipos_servico = (
        TipoServicoService.listar_completo(
            request.args
        )
    )


    return render_template(

        "tipos_servico/completo.html",

        titulo="Visualização Completa de Tipos de Serviço",

        tipos_servico=tipos_servico,

        campos=FILTROS_TIPO_SERVICO,

        campos_filtro=request.args.getlist(
            "campo[]"
        ),

        valores_filtro=request.args.getlist(
            "valor[]"
        )

    )


def _tipo_servico_formulario(
    nome
):

    from app.models import TipoServico

    return TipoServico(
        nome=nome or ""
    )