from app.models import Usuario, Caminhao, Motorista, Administradora, TipoServico, Cliente, TabelaValores

from app.filters.caminhao import FILTROS_CAMINHAO
from app.filters.motorista import FILTROS_MOTORISTA
from app.filters.usuario import FILTROS_USUARIO
from app.filters.administradora import FILTROS_ADMINISTRADORA
from app.filters.tipo_servico import FILTROS_TIPO_SERVICO
from app.filters.cliente import FILTROS_CLIENTE
from app.filters.tabela_valores import FILTROS_TABELA_VALORES


from app.services.tabela_valores_service import TabelaValoresService



MODELOS_MAPEADOS = {

        "usuario": {

            "modelo": Usuario,

            "titulo": "Usuários",

            "ordenar_por": "nome",

            "filtros_config": FILTROS_USUARIO,

            "colunas_exportacao": [

                "nome",
                "login",
                "perfil",
                "ativo"

            ],

            "labels": {

                "nome": "Nome",

                "login": "Login",

                "perfil": "Perfil",

                "ativo": "Status"

            }

        },

    "caminhao": {

        "modelo": Caminhao,

        "filtros_config": FILTROS_CAMINHAO,

        "ordenar_por": "modelo",

        "titulo": "Caminhões",

        "colunas_exportacao": [

            "placa",

            "modelo",

            "ativo"

        ],

        "labels": {

            "placa": "Placa",

            "modelo": "Modelo",

            "ativo": "Status"

        }

    },

    "motorista": {

        "modelo": Motorista,

        "titulo": "Motoristas",

        "ordenar_por": "nome",

        "filtros_config": FILTROS_MOTORISTA,

        "colunas_exportacao": [

            "matricula",
            "nome",
            "numero_cnh",
            "categoria_cnh",
            "validade_cnh",
            "validade_toxicologico",
            "ativo"

        ],

        "labels": {

            "matricula": "Matrícula",

            "nome": "Nome",

            "numero_cnh": "Número da CNH",

            "categoria_cnh": "Categoria",

            "validade_cnh": "Data de Validade da CNH",

            "validade_toxicologico": "Data de Validade do Toxicológico",

            "ativo": "Status"

        }

    },

    "administradora": {

        "modelo": Administradora,

        "titulo": "Administradoras",

        "ordenar_por": "nome",

        "filtros_config": FILTROS_ADMINISTRADORA,

        "colunas_exportacao": [

            "nome",

            "cliente_proprio",

            "ativo"

        ],

        "labels": {

            "nome": "Nome",

            "cliente_proprio": "Cliente Próprio",

            "ativo": "Status"

        }

    },

    "tipo_servico": {

        "modelo": TipoServico,

        "titulo": "Tipos de Serviço",

        "ordenar_por": "nome",

        "filtros_config": FILTROS_TIPO_SERVICO,

        "colunas_exportacao": [

            "nome",

            "ativo"

        ],

        "labels": {

            "nome": "Nome",

            "ativo": "Status"

        }

    },

    "cliente": {

        "modelo": Cliente,

        "titulo": "Clientes",

        "ordenar_por": "nome_fantasia",

        "filtros_config": FILTROS_CLIENTE,

        "colunas_exportacao": [

            "administradora.nome",

            "nome_fantasia",

            "razao_social",

            "cnpj",

            "ativo"

        ],

        "labels": {

            "administradora.nome": "Administradora",

            "nome_fantasia": "Nome Fantasia",

            "razao_social": "Razão Social",

            "cnpj": "CNPJ",

            "ativo": "Status"

        }

    },

        "tabela_valores": {

        "modelo": TabelaValores,

        "titulo": "Tabelas de Valores",

        "ordenar_por": "fk_administradora_id_administradora",

        "listar_service": TabelaValoresService.listar,

        "filtros_config": FILTROS_TABELA_VALORES,

        "colunas_exportacao": [

            "administradora",

            "quantidade",

            "situacao"

        ],

        "labels": {

            "administradora": "Administradora",

            "quantidade": "Quantidade",

            "situacao": "Situação"

        }

    },

    "tabela_valores_completo": {

        "modelo": TabelaValores,

        "titulo": "Tabelas de Valores",

        "ordenar_por": "fk_administradora_id_administradora",

        "filtros_config": FILTROS_TABELA_VALORES,

        "colunas_exportacao": [

            "administradora.nome",

            "tipo_servico.nome",

            "valor_saida",

            "valor_km_excedente"

        ],

        "labels": {

            "administradora.nome": "Administradora",

            "tipo_servico.nome": "Tipo de Serviço",

            "valor_saida": "Valor de Saída",

            "valor_km_excedente": "KM Excedente"

        }

    }
}