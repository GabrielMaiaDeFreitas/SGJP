from copy import deepcopy
from datetime import date
from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash,
    jsonify
)

from app.models import Usuario

from app.services.atendimento_service import (
    AtendimentoService
)

from app.services.cliente_service import (
    ClienteService
)

from app.filters.atendimento import (
    FILTROS_ATENDIMENTO
)

from app.constants.atendimento import (
    VALOR_PATINS,
    VALOR_HORA_PARADA,
    VALOR_HORA_TRABALHADA,
    KM_FRANQUIA
)

from app.helpers.autorizacao_helper import (
    proteger_blueprint
)

from app.exceptions.validacao import ValidacaoError
from app.exceptions.negocio import RegraNegocioError


atendimento_bp = Blueprint(
    "atendimento",
    __name__,
    url_prefix="/atendimentos"
)


proteger_blueprint(
    atendimento_bp,
    "Administrador",
    "Operador"
)

# =========================================================
# REPOPULAÇÃO DO FORMULÁRIO APÓS ERRO
# =========================================================

def _int_ou_none(valor):

    try:

        return int(valor)

    except (TypeError, ValueError):

        return None


def _date_ou_none(valor):

    if not valor:

        return None

    try:

        return date.fromisoformat(valor)

    except ValueError:

        return None


def _decimal_ou_none(valor):

    if valor is None or str(valor).strip() == "":

        return None

    try:

        return Decimal(str(valor))

    except (InvalidOperation, ValueError):

        return None


def _construir_atendimento_repovoado(form):
    """
    Monta uma estrutura equivalente a um Atendimento
    a partir dos dados enviados no POST, para o template
    conseguir repopular o formulário com o que o usuário
    digitou, em vez de resetar tudo após um erro.
    """

    tem_veiculo = bool(
        (form.get("placa_veiculo_rebocado") or "").strip()
        or
        (form.get("modelo_veiculo_rebocado") or "").strip()
    )

    return {

        "tabela_valores": {

            "fk_administradora_id_administradora":
                _int_ou_none(form.get("id_administradora")),

            "fk_tipo_servico_id_tipo_servico":
                _int_ou_none(form.get("id_tipo_servico")),

        },

        "data_atendimento":
            _date_ou_none(form.get("data_atendimento")),

        "protocolo":
            form.get("protocolo", ""),

        "fk_motorista_id_motorista":
            _int_ou_none(form.get("id_motorista")),

        "fk_caminhao_id_caminhao":
            _int_ou_none(form.get("id_caminhao")),

        "fk_cliente_id_cliente":
            _int_ou_none(form.get("id_cliente")),

        "veiculo_rebocado": {
            "placa": form.get("placa_veiculo_rebocado", ""),
            "modelo": form.get("modelo_veiculo_rebocado", ""),
        } if tem_veiculo else {},

        "origem":
            form.get("origem", ""),

        "destino":
            form.get("destino", ""),

        "valor_total":
            _decimal_ou_none(form.get("valor_total")),

        "status_financeiro":
            "Outro"
            if form.get("pagamento_separado") == "on"
            else "Aguardando Fechamento",

        "valor_pago":
            _decimal_ou_none(form.get("valor_pago")) or Decimal("0"),

        "valor_pedagio":
            _decimal_ou_none(form.get("valor_pedagio")) or Decimal("0"),

        "cobrar_pedagio":
            form.get("cobrar_pedagio") == "on",

        "cobrar_hora_parada":
            form.get("cobrar_hora_parada") == "on",

        "quantidade_hora_parada":
            _int_ou_none(form.get("quantidade_hora_parada")) or 0,

        "cobrar_hora_trabalhada":
            form.get("cobrar_hora_trabalhada") == "on",

        "quantidade_hora_trabalhada":
            _int_ou_none(form.get("quantidade_hora_trabalhada")) or 0,

        "usar_patins":
            form.get("usar_patins") == "on",

        "quantidade_patins":
            _int_ou_none(form.get("quantidade_patins")) or 0,

        "observacao":
            form.get("observacao", ""),

    }


def _construir_atendimento_json_repovoado(form):

    return {

        "fk_cliente_id_cliente":
            _int_ou_none(form.get("id_cliente")),

    }

# =========================================================
# LISTAGEM
# =========================================================

@atendimento_bp.route("/")
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


# =========================================================
# NOVO
# =========================================================

@atendimento_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
def novo():

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    dados_formulario = (
        AtendimentoService.carregar_formulario()
    )

    if request.method == "POST":

        try:

            dados = (
                AtendimentoService.montar_dados(
                    request.form
                )
            )

            AtendimentoService.salvar(

                dados=dados,

                id_usuario=session["usuario_id"]

            )

        except (
            ValidacaoError,
            RegraNegocioError
        ) as erro:

            flash(
                erro.mensagem,
                "warning"
            )

            return render_template(

                "atendimentos/form.html",

                titulo="Novo Atendimento",

                modo_edicao=False,

                atendimento=_construir_atendimento_repovoado(
                    request.form
                ),

                atendimento_json=_construir_atendimento_json_repovoado(
                    request.form
                ),

                **dados_formulario,

                data_atual=date.today(),

                VALOR_PATINS=float(VALOR_PATINS),
                VALOR_HORA_PARADA=float(VALOR_HORA_PARADA),
                VALOR_HORA_TRABALHADA=float(VALOR_HORA_TRABALHADA),
                KM_FRANQUIA=KM_FRANQUIA

            )

        flash(

            "Atendimento cadastrado com sucesso.",

            "success"

        )

        return redirect(

            url_for(
                "atendimento.listar"
            )

        )

    return render_template(

        "atendimentos/form.html",

        titulo="Novo Atendimento",

        **dados_formulario,

        data_atual=date.today(),

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


# =========================================================
# EDITAR
# =========================================================

@atendimento_bp.route(
    "/<int:id_atendimento>/editar",
    methods=["GET", "POST"]
)
def editar(id_atendimento):

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    atendimento = (
        AtendimentoService.detalhes(
            id_atendimento
        )
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
            float(
                atendimento.valor_total or 0
            ),

        "km_total":
            float(
                atendimento.km_total or 0
            )

    }

    if request.method == "POST":

        try:

            dados = (
                AtendimentoService.montar_dados(
                    request.form
                )
            )

            AtendimentoService.atualizar(

                atendimento=atendimento,

                dados=dados

            )

        except (
            ValidacaoError,
            RegraNegocioError
        ) as erro:

            flash(
                erro.mensagem,
                "warning"
            )

            return render_template(

                "atendimentos/form.html",

                titulo="Editar Atendimento",

                atendimento=_construir_atendimento_repovoado(
                    request.form
                ),

                atendimento_json=_construir_atendimento_json_repovoado(
                    request.form
                ),

                modo_edicao=True,

                **dados_formulario,

                data_atual=date.today(),

                VALOR_PATINS=float(VALOR_PATINS),
                VALOR_HORA_PARADA=float(VALOR_HORA_PARADA),
                VALOR_HORA_TRABALHADA=float(VALOR_HORA_TRABALHADA),
                KM_FRANQUIA=KM_FRANQUIA

            )

        flash(

            "Atendimento atualizado com sucesso.",

            "success"

        )

        return redirect(

            url_for(

                "atendimento.detalhes",

                id_atendimento=(
                    atendimento.id_atendimento
                )

            )

        )

    return render_template(

        "atendimentos/form.html",

        titulo="Editar Atendimento",

        atendimento=atendimento,

        atendimento_json=atendimento_json,

        **dados_formulario,

        modo_edicao=True,

        data_atual=date.today(),

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


# =========================================================
# DETALHES
# =========================================================

@atendimento_bp.route(
    "/<int:id_atendimento>"
)
def detalhes(id_atendimento):

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    atendimento = (
        AtendimentoService.detalhes(
            id_atendimento
        )
    )

    return render_template(

        "atendimentos/detalhes.html",

        titulo="Detalhes do Atendimento",

        atendimento=atendimento

    )


# =========================================================
# VISUALIZAÇÃO COMPLETA
# =========================================================

@atendimento_bp.route("/completo")
def completo():

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )


    atendimentos = (
        AtendimentoService.listar_completo(
            request.args
        )
    )


    campos = deepcopy(
        FILTROS_ATENDIMENTO
    )


    dados_formulario = (
        AtendimentoService.carregar_formulario()
    )


    _preencher_opcoes_filtros_atendimento(

        campos,

        dados_formulario

    )


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
        ),

        **dados_formulario

    )


# =========================================================
# EXCLUIR
# =========================================================

@atendimento_bp.route(
    "/<int:id_atendimento>/excluir",
    methods=["POST"]
)
def excluir(id_atendimento):

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    if session.get("perfil") != "Administrador":

        flash(

            "Apenas administradores podem "
            "excluir atendimentos.",

            "warning"

        )

        return redirect(

            url_for(
                "atendimento.listar"
            )

        )

    AtendimentoService.excluir(
        id_atendimento
    )

    flash(

        "Atendimento excluído com sucesso.",

        "success"

    )

    return redirect(

        url_for(
            "atendimento.listar"
        )

    )


# =========================================================
# REGISTRAR PAGAMENTO
# =========================================================

@atendimento_bp.route(
    "/<int:id_atendimento>/registrar-pagamento",
    methods=["POST"]
)
def registrar_pagamento(id_atendimento):

    if "usuario_id" not in session:

        return redirect(
            url_for("autenticacao.login")
        )

    atendimento = (
        AtendimentoService.detalhes(
            id_atendimento
        )
    )

    AtendimentoService.registrar_pagamento(
        [atendimento]
    )

    flash(

        "Pagamento registrado com sucesso.",

        "success"

    )

    origem = request.form.get(
        "origem"
    )

    if origem == "detalhes":

        return redirect(

            url_for(

                "atendimento.detalhes",

                id_atendimento=id_atendimento

            )

        )

    return redirect(

        request.referrer
        or
        url_for(
            "atendimento.listar"
        )

    )


# =========================================================
# TABELA DE VALORES
# =========================================================

@atendimento_bp.route(
    "/tabela-valores"
)
def tabela_valores():

    if "usuario_id" not in session:

        return jsonify(
            {
                "erro": "Não autenticado"
            }
        ), 401

    id_administradora = request.args.get(
        "id_administradora",
        type=int
    )

    id_tipo_servico = request.args.get(
        "id_tipo_servico",
        type=int
    )

    tabela = (
        AtendimentoService.buscar_tabela_valores(

            id_administradora,

            id_tipo_servico

        )
    )

    if tabela is None:

        return jsonify(None)

    return jsonify({

        "valor_saida": float(
            tabela.valor_saida or 0
        ),

        "valor_km_excedente": float(
            tabela.valor_km_excedente or 0
        )

    })


# =========================================================
# CLIENTES
# =========================================================

@atendimento_bp.route(
    "/clientes"
)
def clientes():

    if "usuario_id" not in session:

        return jsonify(
            {
                "erro": "Não autenticado"
            }
        ), 401

    id_administradora = request.args.get(
        "id_administradora",
        type=int
    )

    dados = (
        ClienteService.listar_por_administradora(
            id_administradora
        )
    )

    return jsonify(
        dados
    )


# =========================================================
# CALCULAR DISTÂNCIA
# =========================================================

@atendimento_bp.route(
    "/calcular-distancia",
    methods=["POST"]
)
def calcular_distancia():

    if "usuario_id" not in session:

        return jsonify(
            {
                "erro": "Não autenticado"
            }
        ), 401

    dados = request.get_json(
        silent=True
    ) or {}

    origem = dados.get(
        "origem"
    )

    destino = dados.get(
        "destino"
    )

    try:

        resultado = (
            AtendimentoService.calcular_distancia(

                origem,

                destino

            )
        )

        return jsonify({

            "km": resultado

        })

    except (
        ValidacaoError,
        RegraNegocioError
    ) as erro:

        return jsonify({

            "erro": erro.mensagem

        }), 400

def _preencher_opcoes_filtros_atendimento(
    campos,
    dados_formulario
):

    administradoras = (
        dados_formulario["administradoras"]
    )

    clientes = (
        dados_formulario["clientes"]
    )

    tipos_servico = (
        dados_formulario["tipos_servico"]
    )

    motoristas = (
        dados_formulario["motoristas"]
    )

    caminhoes = (
        dados_formulario["caminhoes"]
    )

    usuarios = (
        Usuario.query
            .filter_by(
                ativo=True
            )
            .order_by(
                Usuario.nome
            )
            .all()
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

                for administradora
                in administradoras

            ]


        elif (
            campo["campo"]
            == "fk_cliente_id_cliente"
        ):

            campo["opcoes"] = [

                {
                    "id":
                        cliente.id_cliente,

                    "label":
                        cliente.nome_fantasia

                }

                for cliente
                in clientes

            ]


        elif (
            campo["campo"]
            == "fk_usuario_id_usuario"
        ):

            campo["opcoes"] = [

                {
                    "id":
                        usuario.id_usuario,

                    "label":
                        usuario.nome

                }

                for usuario
                in usuarios

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

                for tipo
                in tipos_servico

            ]


        elif (
            campo["campo"]
            == "fk_motorista_id_motorista"
        ):

            campo["opcoes"] = [

                {
                    "id":
                        motorista.id_motorista,

                    "label":
                        motorista.nome

                }

                for motorista
                in motoristas

            ]


        elif (
            campo["campo"]
            == "fk_caminhao_id_caminhao"
        ):

            campo["opcoes"] = [

                {
                    "id":
                        caminhao.id_caminhao,

                    "label":
                        caminhao.placa

                }

                for caminhao
                in caminhoes

            ]