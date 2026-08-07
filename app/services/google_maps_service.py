import requests

from app.services.coordenada_service import (
    CoordenadaService
)

from app.constants.google_maps import (
    GOOGLE_MAPS_API_KEY,
    URL_ROUTES,
    FIELD_MASK,
    LATITUDE_BASE,
    LONGITUDE_BASE,
    TRAVEL_MODE
)


class GoogleMapsService:

    URL = URL_ROUTES

    @staticmethod
    def calcular_distancia(

        origem,

        destino

    ):

        origem = CoordenadaService.converter(

            origem

        )

        destino = CoordenadaService.converter(

            destino

        )

        body = GoogleMapsService._montar_body(

            origem,

            destino

        )

        resposta = requests.post(

            GoogleMapsService.URL,

            headers=GoogleMapsService._headers(),

            json=body,

            timeout=20

        )

        resposta.raise_for_status()

        return GoogleMapsService._extrair_distancia(

            resposta.json()

        )

    @staticmethod
    def _headers():

        if not GOOGLE_MAPS_API_KEY:

            raise RuntimeError(

                "GOOGLE_MAPS_API_KEY não configurada."

            )

        return {

            "Content-Type":

                "application/json",

            "X-Goog-Api-Key":

                GOOGLE_MAPS_API_KEY,

            "X-Goog-FieldMask":

                FIELD_MASK

        }

    @staticmethod
    def _montar_body(

        origem,

        destino

    ):

        return {

            "origin": {

                "location": {

                    "latLng": {

                        "latitude":

                            LATITUDE_BASE,

                        "longitude":

                            LONGITUDE_BASE

                    }

                }

            },

            "destination": {

                "location": {

                    "latLng": {

                        "latitude":

                            LATITUDE_BASE,

                        "longitude":

                            LONGITUDE_BASE

                    }

                }

            },

            "intermediates": [

                {

                    "location": {

                        "latLng": {

                            "latitude":

                                origem[0],

                            "longitude":

                                origem[1]

                        }

                    }

                },

                {

                    "location": {

                        "latLng": {

                            "latitude":

                                destino[0],

                            "longitude":

                                destino[1]

                        }

                    }

                }

            ],

            "travelMode":

                TRAVEL_MODE

        }

    @staticmethod
    def _extrair_distancia(

        resposta

    ):

        metros = (

            resposta["routes"][0]

            ["distanceMeters"]

        )

        return round(

            metros / 1000,

            2

        )

