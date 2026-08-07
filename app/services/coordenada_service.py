import re


class CoordenadaService:

    @staticmethod
    def converter(texto):

        texto = texto.strip()

        if "°" in texto:

            return CoordenadaService._converter_graus(
                texto
            )

        return CoordenadaService._converter_decimal(
            texto
        )

    @staticmethod
    def _converter_decimal(texto):

        latitude, longitude = texto.split(",")

        return (

            float(latitude.strip()),

            float(longitude.strip())

        )

    @staticmethod
    def _converter_graus(texto):

        padrao = (

            r"(\d+)°\s*"

            r"(\d+)'\s*"

            r"([\d.]+)\"?\s*"

            r"([NS])"

            r"\s*,?\s*"

            r"(\d+)°\s*"

            r"(\d+)'\s*"

            r"([\d.]+)\"?\s*"

            r"([EW])"

        )

        resultado = re.match(

            padrao,

            texto

        )

        if resultado is None:

            raise ValueError(

                "Coordenada inválida."

            )

        grupos = resultado.groups()

        latitude = CoordenadaService._dms_para_decimal(

            int(grupos[0]),

            int(grupos[1]),

            float(grupos[2]),

            grupos[3]

        )

        longitude = CoordenadaService._dms_para_decimal(

            int(grupos[4]),

            int(grupos[5]),

            float(grupos[6]),

            grupos[7]

        )

        return (

            latitude,

            longitude

        )

    @staticmethod
    def _dms_para_decimal(

        graus,

        minutos,

        segundos,

        direcao

    ):

        decimal = (

            graus +

            minutos / 60 +

            segundos / 3600

        )

        if direcao in (

            "S",

            "W"

        ):

            decimal *= -1

        return decimal