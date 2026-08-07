from app.models import (
    Cliente,
    Administradora
)

from app.filters.cliente import (
    FILTROS_CLIENTE
)

from app.services.filter_service import (
    FilterService
)


class ClienteService:

    @staticmethod
    def listar(filtros):

        return FilterService.listar(

            modelo=Cliente,

            filtros=filtros,

            configuracoes=FILTROS_CLIENTE,

            ordenar_por="nome_fantasia"

        )

    @staticmethod
    def listar_por_administradora(

        id_administradora

    ):

        administradora = Administradora.query.get_or_404(

            id_administradora

        )

        clientes = Cliente.query.filter_by(

            ativo=True,

            fk_administradora_id_administradora=(
                id_administradora
            )

        ).order_by(

            Cliente.nome_fantasia

        ).all()

        return {

            "cliente_proprio": (

                administradora.cliente_proprio

            ),

            "clientes": [

                {

                    "id": cliente.id_cliente,

                    "nome": cliente.nome_fantasia

                }

                for cliente in clientes

            ]

        }