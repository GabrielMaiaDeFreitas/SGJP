from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

from copy import deepcopy
from flask import jsonify

from app.models import (
    Atendimento,
    Administradora,
    Motorista,
    Caminhao,
    Cliente,
    TipoServico,
    Usuario
)

from app.filters.atendimento import (
    FILTROS_ATENDIMENTO
)

from app.services.atendimento_service import (
    AtendimentoService
)

from app.services.cliente_service import (
    ClienteService
)

from app.helpers.autorizacao_helper import (
    requer_perfil
)

from app.constants.atendimento import (
    VALOR_PATINS,
    VALOR_HORA_PARADA,
    VALOR_HORA_TRABALHADA,
    KM_FRANQUIA
)


atendimento_bp = Blueprint(

    "atendimento",

    __name__,

    url_prefix="/atendimentos"

)

@atendimento_bp.route("/")
@requer_perfil("Administrador","Operador")
def listar():

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    atendimentos = AtendimentoService.listar()

    return render_template(

        "atendimentos/listar.html",

        titulo="Gerenciamento de Atendimentos",

        atendimentos=atendimentos,

        novo_url=url_for(
            "atendimento.novo"
        ),

        novo_texto="Novo Atendimento",

        visualizacao_url=url_for(
            "atendimento.completo"
        ),

        exportar_url=url_for(
            "exportacao.exportar_generico",
            modulo="atendimento"
        )

    )

@atendimento_bp.route("/novo",methods=["GET", "POST"])
@requer_perfil("Administrador","Operador")
def novo():

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    dados_formulario = (

        AtendimentoService.carregar_formulario()

    )

    if request.method == "POST":

        dados = AtendimentoService.montar_dados(

            request.form

        )

        try:

            AtendimentoService.salvar(

                dados=dados,

                id_usuario=session["usuario_id"]

            )

        except ValueError as erro:

            flash(

                str(erro),

                "warning"

            )

            return render_template(

                "atendimentos/form.html",

                titulo="Novo Atendimento",

                **dados_formulario,

                VALOR_PATINS=float(
                    VALOR_PATINS
                ),

                VALOR_HORA_PARADA=float(
                    VALOR_HORA_PARADA
                ),

                VALOR_HORA_TRABALHADA=float(
                    VALOR_HORA_TRABALHADA
                ),

                KM_FRANQUIA=KM_FRANQUIA,

                resetar_novo_atendimento=False

            )

        flash(

            "Atendimento cadastrado com sucesso.",

            "success"

        )

        return render_template(

            "atendimentos/form.html",

            titulo="Novo Atendimento",

            **dados_formulario,

            VALOR_PATINS=float(
                VALOR_PATINS
            ),

            VALOR_HORA_PARADA=float(
                VALOR_HORA_PARADA
            ),

            VALOR_HORA_TRABALHADA=float(
                VALOR_HORA_TRABALHADA
            ),

            KM_FRANQUIA=KM_FRANQUIA,

            resetar_novo_atendimento=True,

            administradora_inicial=(
                dados["id_administradora"]
            ),

            data_atendimento_inicial=(
                dados["data_atendimento"]
            )

        )

    return render_template(

        "atendimentos/form.html",

        titulo="Novo Atendimento",

        **dados_formulario,

        VALOR_PATINS=float(
            VALOR_PATINS
        ),

        VALOR_HORA_PARADA=float(
            VALOR_HORA_PARADA
        ),

        VALOR_HORA_TRABALHADA=float(
            VALOR_HORA_TRABALHADA
        ),

        KM_FRANQUIA=KM_FRANQUIA,

        resetar_novo_atendimento=False

    )

@atendimento_bp.route(
    "/<int:id_atendimento>/editar",
    methods=["GET", "POST"]
)
@requer_perfil("Administrador","Operador")
def editar(id_atendimento):

    if "usuario_id" not in session:

        return redirect(

            url_for("autenticacao.login")

        )

    atendimento = AtendimentoService.detalhes(

        id_atendimento

    )

    dados_formulario = (

        AtendimentoService.carregar_formulario()

    )

    atendimento_json = {

        "fk_cliente_id_cliente":

            atendimento.fk_cliente_id_cliente,

        "fk_motorista_id_motorista":

            atendimento.fk_motorista_id_motorista,

        "fk_caminhao_id_caminhao":

            atendimento.fk_caminhao_id_caminhao,

        "fk_tabela_valores_id_tabela_valores":

            atendimento.fk_tabela_valores_id_tabela_valores,

        "valor_total":

            float(atendimento.valor_total or 0),

        "km_total":

            float(atendimento.km_total or 0)

    }

    if request.method == "POST":

        dados = AtendimentoService.montar_dados(

            request.form

        )

        try:

            AtendimentoService.atualizar(

                atendimento=atendimento,

                dados=dados

            )

        except ValueError as erro:

            flash(

                str(erro),

                "warning"

            )

            return render_template(

                "atendimentos/form.html",

                titulo="Editar Atendimento",

                atendimento=atendimento,

                atendimento_json=atendimento_json,

                **dados_formulario,

                VALOR_PATINS=float(

                    VALOR_PATINS

                ),

                VALOR_HORA_PARADA=float(

                    VALOR_HORA_PARADA

                ),

                VALOR_HORA_TRABALHADA=float(

                    VALOR_HORA_TRABALHADA

                ),

                KM_FRANQUIA=KM_FRANQUIA

            )

        flash(

            "Atendimento atualizado com sucesso.",

            "success"

        )

        return redirect(

            url_for(

                "atendimento.detalhes",

                id_atendimento=atendimento.id_atendimento

            )

        )

    return render_template(

        "atendimentos/form.html",

        titulo="Editar Atendimento",

        atendimento=atendimento,

        atendimento_json=atendimento_json,

        **dados_formulario,

        VALOR_PATINS=float(

            VALOR_PATINS

        ),

        VALOR_HORA_PARADA=float(

            VALOR_HORA_PARADA

        ),

        VALOR_HORA_TRABALHADA=float(

            VALOR_HORA_TRABALHADA

        ),

        KM_FRANQUIA=KM_FRANQUIA

    )

@atendimento_bp.route("/<int:id_atendimento>")
@requer_perfil("Administrador","Operador")
def detalhes(id_atendimento):

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    atendimento = AtendimentoService.detalhes(

        id_atendimento

    )

    return render_template(

        "atendimentos/detalhes.html",

        titulo="Detalhes do Atendimento",

        atendimento=atendimento

    )

@atendimento_bp.route("/completo")
@requer_perfil("Administrador","Operador")
def completo():

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    atendimentos = AtendimentoService.listar_completo(

        request.args

    )

    campos = deepcopy(

        FILTROS_ATENDIMENTO

    )

    administradoras = Administradora.query.filter_by(

        ativo=True

    ).order_by(

        Administradora.nome

    ).all()

    clientes = Cliente.query.filter_by(

        ativo=True

    ).order_by(

        Cliente.nome_fantasia

    ).all()

    tipos_servico = TipoServico.query.filter_by(

        ativo=True

    ).order_by(

        TipoServico.nome

    ).all()

    motoristas = Motorista.query.filter_by(

        ativo=True

    ).order_by(

        Motorista.nome

    ).all()

    caminhoes = Caminhao.query.filter_by(

        ativo=True

    ).order_by(

        Caminhao.placa

    ).all()

    usuarios = Usuario.query.filter_by(

        ativo=True

    ).order_by(

        Usuario.nome

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

        elif campo["campo"] == "fk_cliente_id_cliente":

            campo["opcoes"] = [

                {

                    "id": cliente.id_cliente,

                    "label": cliente.nome_fantasia

                }

                for cliente in clientes

            ]

        elif campo["campo"] == "fk_usuario_id_usuario":

            campo["opcoes"] = [

                {

                    "id": usuario.id_usuario,

                    "label": usuario.nome

                }

                for usuario in usuarios

            ]

        elif campo["campo"] == "fk_tipo_servico_id_tipo_servico":

            campo["opcoes"] = [

                {

                    "id": tipo.id_tipo_servico,

                    "label": tipo.nome

                }

                for tipo in tipos_servico

            ]

        elif campo["campo"] == "fk_motorista_id_motorista":

            campo["opcoes"] = [

                {

                    "id": motorista.id_motorista,

                    "label": motorista.nome

                }

                for motorista in motoristas

            ]

        elif campo["campo"] == "fk_caminhao_id_caminhao":

            campo["opcoes"] = [

                {

                    "id": caminhao.id_caminhao,

                    "label": caminhao.placa

                }

                for caminhao in caminhoes

            ]

    return render_template(

        "atendimentos/completo.html",

        titulo="Visualização Completa de Atendimentos",

        atendimentos=atendimentos,

        campos=campos,

        campos_filtro=request.args.getlist(

            "campo[]"

        ),

        valores_filtro=request.args.getlist(

            "valor[]"

        )

    )

@atendimento_bp.route(
    "/<int:id_atendimento>/excluir",
    methods=["POST"]
)
@requer_perfil("Administrador")
def excluir(id_atendimento):

    if "usuario_id" not in session:

        return redirect(

            url_for("autenticacao.login")

        )

    AtendimentoService.excluir(

        id_atendimento

    )

    flash(

        "Atendimento excluído com sucesso.",

        "success"

    )

    return redirect(

        url_for("atendimento.listar")

    )

@atendimento_bp.route("/<int:id_atendimento>/registrar-pagamento",methods=["POST"])
@requer_perfil("Administrador")
def registrar_pagamento(id_atendimento):

    if "usuario_id" not in session:

        return redirect(

            url_for("autenticacao.login")

        )

    atendimento = AtendimentoService.detalhes(

        id_atendimento

    )

    AtendimentoService.registrar_pagamento(

        [atendimento]

    )

    flash(

        "Pagamento registrado com sucesso.",

        "success"

    )

    origem = request.form.get("origem")

    if origem == "detalhes":

        return redirect(

            url_for(

                "atendimento.detalhes",

                id_atendimento=id_atendimento

            )

        )

    if origem == "completo":

        return redirect(

            request.referrer
            or url_for(
                "atendimento.completo"
            )

        )

    if origem == "listar":

        return redirect(

            request.referrer
            or url_for(
                "atendimento.listar"
            )

        )

    return redirect(

        request.referrer
        or url_for(
            "atendimento.listar"
        )

    )

@atendimento_bp.route("/tabela-valores")
@requer_perfil("Administrador","Operador")
def tabela_valores():

    if "usuario_id" not in session:

        return jsonify(
            {"erro": "Não autenticado"}
        ), 401

    id_administradora = request.args.get(

        "id_administradora",

        type=int

    )

    id_tipo_servico = request.args.get(

        "id_tipo_servico",

        type=int

    )

    tabela = AtendimentoService.buscar_tabela_valores(

        id_administradora,

        id_tipo_servico

    )

    if tabela is None:

        return jsonify(None)

    return jsonify({

        "valor_saida": float(

            tabela.valor_saida

        ),

        "valor_km_excedente": float(

            tabela.valor_km_excedente

        )

    })

@atendimento_bp.route("/clientes")
@requer_perfil("Administrador","Operador")
def clientes():

    if "usuario_id" not in session:

        return jsonify(

            {"erro": "Não autenticado"}

        ), 401

    id_administradora = request.args.get(

        "id_administradora",

        type=int

    )

    dados = ClienteService.listar_por_administradora(

        id_administradora

    )

    return jsonify(dados)



@atendimento_bp.route("/calcular-distancia", methods=["POST"])
def calcular_distancia():

    if "usuario_id" not in session:

        return jsonify(

            {"erro": "Não autenticado"}

        ), 401

    dados = request.get_json()

    try:

        km = AtendimentoService.calcular_distancia(

            origem=dados["origem"],

            destino=dados["destino"]

        )

    except ValueError as erro:

        return jsonify({

            "erro": str(erro)

        }), 400

    return jsonify({

        "km": km

    })