from app.models import Usuario
from app.filters.usuario import FILTROS_USUARIO
from app.services.filter_service import FilterService


class UsuarioService:

    @staticmethod
    def listar(filtros):

        return FilterService.listar(

            modelo=Usuario,

            filtros=filtros,

            configuracoes=FILTROS_USUARIO,

            ordenar_por="nome"

        )