from datetime import date


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

        campos = filtros.getlist(
            "campo[]"
        )

        valores = filtros.getlist(
            "valor[]"
        )

        valores_min = filtros.getlist(
            "valor_min[]"
        )

        valores_max = filtros.getlist(
            "valor_max[]"
        )

        indice_valor = 0
        indice_min = 0
        indice_max = 0

        for campo in campos:

            configuracao = configuracoes.get(
                campo
            )

            if configuracao is None:
                continue

            tipo = configuracao.get(
                "tipo"
            )

            subtipo = configuracao.get(
                "subtipo"
            )

            if tipo == "intervalo":

                valor_min = (
                    valores_min[indice_min]
                    if indice_min < len(valores_min)
                    else ""
                )

                valor_max = (
                    valores_max[indice_max]
                    if indice_max < len(valores_max)
                    else ""
                )

                indice_min += 1
                indice_max += 1

                if not valor_min and not valor_max:
                    continue

                valor = ""

            else:

                valor = (
                    valores[indice_valor]
                    if indice_valor < len(valores)
                    else ""
                )

                indice_valor += 1

                if not valor:
                    continue

                valor_min = ""
                valor_max = ""

            atributo_config = configuracao.get(
                "atributo",
                configuracao["campo"]
            )

            query, atributo = (
                FilterService._obter_atributo(
                    query,
                    modelo,
                    atributo_config
                )
            )

            operacao = configuracao.get(
                "operacao",
                "igual"
            )

            if configuracao.get(
                "converter"
            ) == "boolean":

                valor = (
                    valor == "Ativo"
                )

            if configuracao.get(
                "converter"
            ) == "cliente_proprio":

                valor = (
                    valor == "Sim"
                )

            if configuracao.get(
                "converter"
            ) == "sim_nao":

                valor = (
                    valor == "Sim"
                )

            if tipo == "intervalo":

                if valor_min:

                    valor_min = (
                        FilterService._converter_valor(
                            valor_min,
                            subtipo
                        )
                    )

                    query = query.filter(
                        atributo >= valor_min
                    )

                if valor_max:

                    valor_max = (
                        FilterService._converter_valor(
                            valor_max,
                            subtipo
                        )
                    )

                    query = query.filter(
                        atributo <= valor_max
                    )

            else:

                if (
                    configuracao.get("converter")
                    not in (
                        "boolean",
                        "cliente_proprio",
                        "sim_nao"
                    )
                ):

                    valor = (
                        FilterService._converter_valor(
                            valor,
                            subtipo
                        )
                    )

                if operacao == "contains":

                    query = query.filter(
                        atributo.ilike(
                            f"%{valor}%"
                        )
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

    @staticmethod
    def _converter_valor(valor, subtipo):

        if not valor:
            return valor

        if subtipo == "data":
            return date.fromisoformat(valor)

        if subtipo == "numero":
            return float(valor)

        if subtipo == "inteiro":
            return int(valor)

        if subtipo == "boolean":
            return valor in (
                True,
                "true",
                "True",
                "1",
                1,
                "Sim",
                "Ativo"
            )

        return valor

    @staticmethod
    def _obter_atributo(
        query,
        modelo,
        atributo_config
    ):

        partes = atributo_config.split(".")

        modelo_atual = modelo

        for relacionamento in partes[:-1]:

            atributo_relacionamento = getattr(
                modelo_atual,
                relacionamento
            )

            modelo_relacionado = (
                atributo_relacionamento
                .property
                .mapper
                .class_
            )

            query = query.join(
                atributo_relacionamento
            )

            modelo_atual = (
                modelo_relacionado
            )

        atributo = getattr(
            modelo_atual,
            partes[-1]
        )

        return (
            query,
            atributo
        )