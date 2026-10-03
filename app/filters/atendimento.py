from app.constants.atendimento import (
    STATUS_OPERACIONAL,
    STATUS_FINANCEIRO
)


FILTROS_ATENDIMENTO = [

    {
        "campo": "data_atendimento",
        "atributo": "data_atendimento",
        "label": "Data",
        "tipo": "intervalo",
        "subtipo": "data"
    },

    {
        "campo": "fk_administradora_id_administradora",
        "atributo": (
            "tabela_valores."
            "fk_administradora_id_administradora"
        ),
        "label": "Administradora",
        "tipo": "select",
        "subtipo": "inteiro",
        "operacao": "igual",
        "opcoes": []
    },

    {
        "campo": "fk_cliente_id_cliente",
        "atributo": "fk_cliente_id_cliente",
        "label": "Cliente",
        "tipo": "select",
        "subtipo": "inteiro",
        "operacao": "igual",
        "opcoes": []
    },

    {
        "campo": "fk_usuario_id_usuario",
        "atributo": "fk_usuario_id_usuario",
        "label": "Usuário",
        "tipo": "select",
        "subtipo": "inteiro",
        "operacao": "igual",
        "opcoes": []
    },

    {
        "campo": "fk_tipo_servico_id_tipo_servico",
        "atributo": (
            "tabela_valores."
            "fk_tipo_servico_id_tipo_servico"
        ),
        "label": "Tipo de Serviço",
        "tipo": "select",
        "subtipo": "inteiro",
        "operacao": "igual",
        "opcoes": []
    },

    {
        "campo": "fk_motorista_id_motorista",
        "atributo": "fk_motorista_id_motorista",
        "label": "Motorista",
        "tipo": "select",
        "subtipo": "inteiro",
        "operacao": "igual",
        "opcoes": []
    },

    {
        "campo": "fk_caminhao_id_caminhao",
        "atributo": "fk_caminhao_id_caminhao",
        "label": "Caminhão",
        "tipo": "select",
        "subtipo": "inteiro",
        "operacao": "igual",
        "opcoes": []
    },

    {
        "campo": "placa_veiculo_rebocado",
        "atributo": "veiculo_rebocado.placa",
        "label": "Placa Rebocada",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "modelo_veiculo_rebocado",
        "atributo": "veiculo_rebocado.modelo",
        "label": "Modelo Rebocado",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "protocolo",
        "atributo": "protocolo",
        "label": "Protocolo",
        "tipo": "texto",
        "operacao": "igual"
    },

    {
        "campo": "origem",
        "atributo": "origem",
        "label": "Origem",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "destino",
        "atributo": "destino",
        "label": "Destino",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "km_total",
        "atributo": "km_total",
        "label": "KM Rodado",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "valor_total",
        "atributo": "valor_total",
        "label": "Valor Total",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "valor_comissao",
        "atributo": "valor_comissao",
        "label": "Valor Comissão",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "valor_pago",
        "atributo": "valor_pago",
        "label": "Valor Pago",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "valor_pedagio",
        "atributo": "valor_pedagio",
        "label": "Valor Pedágio",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "quantidade_hora_parada",
        "atributo": "quantidade_hora_parada",
        "label": "Quantidade Hora Parada",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "quantidade_hora_trabalhada",
        "atributo": "quantidade_hora_trabalhada",
        "label": "Quantidade Hora Trabalhada",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "quantidade_patins",
        "atributo": "quantidade_patins",
        "label": "Quantidade Patins",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "cobrar_pedagio",
        "atributo": "cobrar_pedagio",
        "label": "Cobrou Pedágio",
        "tipo": "select",
        "subtipo": "boolean",
        "operacao": "igual",
        "converter": "sim_nao",
        "opcoes": [
            "Sim",
            "Não"
        ]
    },

    {
        "campo": "cobrar_hora_parada",
        "atributo": "cobrar_hora_parada",
        "label": "Cobrou Hora Parada",
        "tipo": "select",
        "subtipo": "boolean",
        "operacao": "igual",
        "converter": "sim_nao",
        "opcoes": [
            "Sim",
            "Não"
        ]
    },

    {
        "campo": "cobrar_hora_trabalhada",
        "atributo": "cobrar_hora_trabalhada",
        "label": "Cobrou Hora Trabalhada",
        "tipo": "select",
        "subtipo": "boolean",
        "operacao": "igual",
        "converter": "sim_nao",
        "opcoes": [
            "Sim",
            "Não"
        ]
    },

    {
        "campo": "usar_patins",
        "atributo": "usar_patins",
        "label": "Usou Patins",
        "tipo": "select",
        "subtipo": "boolean",
        "operacao": "igual",
        "converter": "sim_nao",
        "opcoes": [
            "Sim",
            "Não"
        ]
    },

    {
        "campo": "status_operacional",
        "atributo": "status_operacional",
        "label": "Status Operacional",
        "tipo": "select",
        "operacao": "igual",
        "opcoes": STATUS_OPERACIONAL
    },

    {
        "campo": "status_financeiro",
        "atributo": "status_financeiro",
        "label": "Status Financeiro",
        "tipo": "select",
        "operacao": "igual",
        "opcoes": STATUS_FINANCEIRO
    },

    {
        "campo": "observacao",
        "atributo": "observacao",
        "label": "Observação",
        "tipo": "texto",
        "operacao": "contains"
    }

]