class FilterService:

    @staticmethod
    def listar(
        modelo,
        filtros,
        configuracoes,
        ordenar_por
    ):

        query = modelo.query

        configuracoes = {

            filtro["campo"]: filtro

            for filtro in configuracoes

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

                modelo,

                configuracao.get(
                    "atributo",
                    configuracao["campo"]
                )

            )

            operacao = configuracao.get(
                "operacao",
                "igual"
            )

            if (
                configuracao.get("converter")
                == "boolean"
            ):

                valor = valor == "Ativo"

            if (
                configuracao.get("converter")
                == "cliente_proprio"
            ):

                valor = valor == "Sim"

            if operacao == "contains":

                query = query.filter(
                    atributo.ilike(f"%{valor}%")
                )

            elif operacao == "igual":

                query = query.filter(
                    atributo == valor
                )

        atributo_ordenacao = getattr(
            modelo,
            ordenar_por
        )

        return query.order_by(
            atributo_ordenacao
        ).all()