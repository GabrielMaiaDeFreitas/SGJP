from app.models import Administradora
from app.filters.administradora import FILTROS_ADMINISTRADORA
from app.services.filter_service import FilterService


class AdministradoraService:

    @staticmethod
    def listar(filtros):

        return FilterService.listar(

            modelo=Administradora,

            filtros=filtros,

            configuracoes=FILTROS_ADMINISTRADORA,

            ordenar_por="nome"

        )