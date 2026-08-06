class ObjectUtils:

    @staticmethod
    def obter_valor(objeto, caminho):

        valor = objeto

        for atributo in caminho.split("."):

            if valor is None:

                return None

            if isinstance(valor, dict):

                valor = valor.get(atributo)

            else:

                valor = getattr(

                    valor,

                    atributo

                )

        return valor