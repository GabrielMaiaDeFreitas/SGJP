from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

from flask import Response

from app.exports.csv_service import CsvService
from app.exports.excel_service import ExcelService
from app.exports.pdf_service import PdfService


class ZipService:

    @staticmethod
    def exportar(
        dados,
        colunas,
        formatos,
        nome_arquivo,
        titulo,
        labels
    ):

        buffer = BytesIO()

        with ZipFile(
            buffer,
            "w",
            ZIP_DEFLATED
        ) as zip_file:

            for formato in formatos:

                if formato == "excel":

                    resposta = ExcelService.exportar(

                        dados=dados,

                        colunas=colunas,

                        nome_arquivo=nome_arquivo,

                        titulo=titulo,

                        labels=labels

                    )

                    zip_file.writestr(

                        f"{nome_arquivo}.xlsx",

                        resposta.get_data()

                    )

                elif formato == "pdf":

                    resposta = PdfService.exportar(

                        dados=dados,

                        colunas=colunas,

                        nome_arquivo=nome_arquivo,

                        titulo=titulo,

                        labels=labels

                    )

                    zip_file.writestr(

                        f"{nome_arquivo}.pdf",

                        resposta.get_data()

                    )

                elif formato == "csv":

                    resposta = CsvService.exportar(

                        dados=dados,

                        colunas=colunas,

                        nome_arquivo=nome_arquivo,

                        labels=labels

                    )

                    zip_file.writestr(

                        f"{nome_arquivo}.csv",

                        resposta.get_data()

                    )

        buffer.seek(0)

        return Response(

            buffer.getvalue(),

            mimetype="application/zip",

            headers={

                "Content-Disposition":

                f'attachment; filename="{nome_arquivo}.zip"'

            }

        )