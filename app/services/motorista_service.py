from app.models import Motorista
from app.filters.motorista import FILTROS_MOTORISTA
from app.services.filter_service import FilterService



class MotoristaService:

    @staticmethod
    def listar(filtros):

        return FilterService.listar(

            modelo=Motorista,

            filtros=filtros,

            configuracoes=FILTROS_MOTORISTA,

            ordenar_por="nome"

        )