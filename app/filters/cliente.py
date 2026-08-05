from app.constants.common import STATUS


FILTROS_CLIENTE = [

    {
        "campo": "nome_fantasia",
        "atributo": "nome_fantasia",
        "label": "Nome Fantasia",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "razao_social",
        "atributo": "razao_social",
        "label": "Razão Social",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "cnpj",
        "atributo": "cnpj",
        "label": "CNPJ",
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