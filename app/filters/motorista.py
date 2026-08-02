from app.constants.motorista import (
    CATEGORIAS_CNH,
    STATUS
)

FILTROS_MOTORISTA = [
    {
        "campo": "matricula",
        "label": "Matrícula",
        "tipo": "texto"
    },
    {
        "campo": "nome",
        "label": "Nome",
        "tipo": "texto"
    },
    {
        "campo": "numero_cnh",
        "label": "Número da CNH",
        "tipo": "texto"
    },
    {
        "campo": "categoria_cnh",
        "label": "Categoria",
        "tipo": "select",
        "opcoes": CATEGORIAS_CNH
    },
    {
        "campo": "validade_cnh",
        "label": "Validade CNH",
        "tipo": "data"
    },
    {
        "campo": "validade_toxicologico",
        "label": "Validade Toxicológico",
        "tipo": "data"
    },
    {
        "campo": "ativo",
        "label": "Status",
        "tipo": "select",
        "opcoes": STATUS
    }
]