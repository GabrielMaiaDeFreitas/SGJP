from app.models import Motorista
from app.filters.motorista import FILTROS_MOTORISTA


class MotoristaService:

    @staticmethod
    def listar(filtros):

        query = Motorista.query

        configuracoes = {

            filtro["campo"]: filtro

            for filtro in FILTROS_MOTORISTA

        }

        campos = filtros.getlist("campo[]")
        valores = filtros.getlist("valor[]")

        for campo, valor in zip(campos, valores):

            if not valor:
                continue

            configuracao = configuracoes.get(campo)

            if configuracao is None:
                continue

            atributo = getattr(
                Motorista,
                configuracao["atributo"]
            )

            operacao = configuracao["operacao"]

            if operacao == "contains":

                query = query.filter(
                    atributo.ilike(f"%{valor}%")
                )

            elif operacao == "igual":

                if configuracao["tipo"] == "select":

                    if configuracao["atributo"] == "ativo":

                        valor = valor == "Ativo"

                query = query.filter(
                    atributo == valor
                )

        return query.order_by(
            Motorista.nome
        ).all()