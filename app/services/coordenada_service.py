import re
import requests


class CoordenadaService:

    @staticmethod
    def converter(texto):

        texto = texto.strip()

        if "maps.app.goo.gl" in texto:
            return CoordenadaService._converter_link_curto(texto)

        if "google.com/maps" in texto or "maps.google.com" in texto:
            return CoordenadaService._converter_link(texto)

        if "°" in texto:
            return CoordenadaService._converter_graus(texto)

        return CoordenadaService._converter_decimal(texto)

    @staticmethod
    def _converter_decimal(texto):

        latitude, longitude = texto.split(",")

        return (
            float(latitude.strip()),
            float(longitude.strip())
        )

    @staticmethod
    def _converter_link(link):

        padrao = r'@(-?\d+\.\d+),(-?\d+\.\d+)'
        resultado = re.search(padrao, link)

        if resultado:
            return (
                float(resultado.group(1)),
                float(resultado.group(2))
            )

        padrao_q = r'[?&]q=(-?\d+\.\d+),(-?\d+\.\d+)'
        resultado = re.search(padrao_q, link)

        if resultado:
            return (
                float(resultado.group(1)),
                float(resultado.group(2))
            )

        raise ValueError("Link do Google Maps inválido.")

    @staticmethod
    def _converter_link_curto(link):

        resposta = requests.get(
            link,
            allow_redirects=True,
            timeout=10
        )

        return CoordenadaService._converter_link(
            resposta.url
        )

    @staticmethod
    def _converter_graus(texto):

        padrao = (
            r"(\d+)°\s*"
            r"(\d+)'\s*"
            r'([\d.]+)"?\s*'
            r"([NS])"
            r"\s*,?\s*"
            r"(\d+)°\s*"
            r"(\d+)'\s*"
            r'([\d.]+)"?\s*'
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

        if direcao in ("S", "W"):
            decimal *= -1

        return decimal