from app.models import Cliente
from app.filters.cliente import FILTROS_CLIENTE
from app.services.filter_service import FilterService


class ClienteService:

    @staticmethod
    def listar(filtros):

        return FilterService.listar(

            modelo=Cliente,

            filtros=filtros,

            configuracoes=FILTROS_CLIENTE,

            ordenar_por="nome_fantasia"

        )