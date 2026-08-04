from app.constants.common import (
    STATUS
)

from app.constants.usuario import (
    PERFIS
)

FILTROS_USUARIO = [

    {
        "campo": "nome",
        "atributo": "nome",
        "label": "Nome",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "login",
        "atributo": "login",
        "label": "Login",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "perfil",
        "atributo": "perfil",
        "label": "Perfil",
        "tipo": "select",
        "operacao": "igual",
        "opcoes": PERFIS
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