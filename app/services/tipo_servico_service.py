from app.models import TipoServico
from app.filters.tipo_servico import FILTROS_TIPO_SERVICO
from app.services.filter_service import FilterService


class TipoServicoService:

    @staticmethod
    def listar(filtros):

        return FilterService.listar(

            modelo=TipoServico,

            filtros=filtros,

            configuracoes=FILTROS_TIPO_SERVICO,

            ordenar_por="nome"

        )