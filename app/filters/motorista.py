from app.constants.motorista import (
    CATEGORIAS_CNH
)

from app.constants.common import (
    STATUS
)


FILTROS_MOTORISTA = [

    {
        "campo": "matricula",
        "atributo": "matricula",
        "label": "Matrícula",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "nome",
        "atributo": "nome",
        "label": "Nome",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "numero_cnh",
        "atributo": "numero_cnh",
        "label": "Número da CNH",
        "tipo": "texto",
        "operacao": "contains"
    },

    {
        "campo": "categoria_cnh",
        "atributo": "categoria_cnh",
        "label": "Categoria",
        "tipo": "select",
        "operacao": "igual",
        "opcoes": CATEGORIAS_CNH
    },

    {
        "campo": "validade_cnh",
        "atributo": "validade_cnh",
        "label": "Validade CNH",
        "tipo": "intervalo",
        "subtipo": "data"
    },

    {
        "campo": "validade_toxicologico",
        "atributo": "validade_toxicologico",
        "label": "Validade Toxicológico",
        "tipo": "intervalo",
        "subtipo": "data"
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