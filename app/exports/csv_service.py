from datetime import date
from datetime import datetime
from io import StringIO

from flask import Response


class CsvService:

    @staticmethod
    def formatar(valor):

        if isinstance(valor, bool):

            return "Ativo" if valor else "Inativo"

        if isinstance(valor, (date, datetime)):

            return valor.strftime("%d/%m/%Y")

        if valor is None:

            return ""

        return str(valor)

    @staticmethod
    def exportar(
        dados,
        colunas,
        nome_arquivo,
        labels
    ):

        buffer = StringIO()

        # Cabeçalho
        buffer.write(

            ";".join(

                labels.get(
                    coluna,
                    coluna
                )

                for coluna in colunas

            )

        )

        buffer.write("\n")

        # Dados
        for registro in dados:

            linha = []

            for coluna in colunas:

                valor = CsvService.formatar(

                    getattr(
                        registro,
                        coluna
                    )

                )

                # Escapa aspas
                valor = valor.replace('"', '""')

                # Coloca entre aspas caso necessário
                if ";" in valor or "\n" in valor:

                    valor = f'"{valor}"'

                linha.append(valor)

            buffer.write(";".join(linha))

            buffer.write("\n")

        return Response(

            buffer.getvalue().encode("utf-8-sig"),

            mimetype="text/csv",

            headers={

                "Content-Disposition":

                f'attachment; filename="{nome_arquivo}.csv"'

            }

        )