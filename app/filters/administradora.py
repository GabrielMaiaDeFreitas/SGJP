from app.constants.administradora import (
    CLIENTE_PROPRIO
)

from app.constants.common import (
    STATUS
)


FILTROS_ADMINISTRADORA = [

    {
        "campo": "nome",
        "atributo": "nome",
        "label": "Nome",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "cliente_proprio",
        "atributo": "cliente_proprio",
        "label": "Cliente Próprio",
        "tipo": "select",
        "operacao": "igual",
        "converter": "cliente_proprio",
        "opcoes": CLIENTE_PROPRIO
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