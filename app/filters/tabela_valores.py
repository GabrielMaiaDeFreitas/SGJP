from app.constants.common import (
    STATUS
)


FILTROS_TABELA_VALORES = [

    {
        "campo": "fk_administradora_id_administradora",
        "atributo": "fk_administradora_id_administradora",
        "label": "Administradora",
        "tipo": "select",
        "operacao": "igual",
        "opcoes": []
    },

    {
        "campo": "fk_tipo_servico_id_tipo_servico",
        "atributo": "fk_tipo_servico_id_tipo_servico",
        "label": "Tipo de Serviço",
        "tipo": "select",
        "operacao": "igual",
        "opcoes": []
    },

    {
        "campo": "valor_saida",
        "atributo": "valor_saida",
        "label": "Valor de Saída",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "valor_km_excedente",
        "atributo": "valor_km_excedente",
        "label": "KM Excedente",
        "tipo": "intervalo",
        "subtipo": "numero"
    },

    {
        "campo": "ativo",
        "atributo": "ativo",
        "label": "Status",
        "tipo": "select",
        "operacao": "igual",
        "converter": "boolean",
        "opcoes": STATUS
    }

]