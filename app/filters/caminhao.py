from app.constants.common import (
    STATUS
)

FILTROS_CAMINHAO = [
    {
        "campo": "placa",
        "atributo": "placa",
        "label": "Placa",
        "tipo": "texto",
        "operacao": "contains"
    },
    {
        "campo": "modelo",
        "atributo": "modelo",
        "label": "Modelo",
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