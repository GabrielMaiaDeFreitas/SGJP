from app.models import Caminhao
from app.filters.caminhao import FILTROS_CAMINHAO
from app.services.filter_service import FilterService


class CaminhaoService:

    @staticmethod
    def listar(filtros):

        return FilterService.listar(

            modelo=Caminhao,

            filtros=filtros,

            configuracoes=FILTROS_CAMINHAO,

            ordenar_por="modelo"

        )