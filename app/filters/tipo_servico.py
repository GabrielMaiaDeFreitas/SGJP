from app.constants.common import STATUS

FILTROS_TIPO_SERVICO = [

    {
        "campo": "nome",
        "atributo": "nome",
        "label": "Nome",
        "tipo": "texto",
        "operacao": "contains"
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