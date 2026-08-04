from datetime import date
from datetime import datetime
from io import BytesIO

from flask import Response

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)


class PdfService:

    @staticmethod
    def formatar(valor):

        if isinstance(valor, bool):

            return "Ativo" if valor else "Inativo"

        if isinstance(valor, (date, datetime)):

            return valor.strftime("%d/%m/%Y")

        return str(valor)

    @staticmethod
    def exportar(
        dados,
        colunas,
        nome_arquivo,
        titulo,
        labels
    ):

        buffer = BytesIO()

        documento = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4)
        )

        estilos = getSampleStyleSheet()

        elementos = []

        elementos.append(

            Paragraph(

                f"<b>{titulo}</b>",

                estilos["Heading1"]

            )

        )

        tabela = [

            [

                labels.get(
                    coluna,
                    coluna
                )

                for coluna in colunas

            ]

        ]

        for registro in dados:

            tabela.append(

                [

                    PdfService.formatar(

                        getattr(

                            registro,

                            coluna

                        )

                    )

                    for coluna in colunas

                ]

            )

        tabela_pdf = Table(tabela)

        tabela_pdf.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#17324F")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.black
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    8
                )

            ])

        )

        elementos.append(tabela_pdf)

        documento.build(elementos)

        buffer.seek(0)

        return Response(

            buffer.getvalue(),

            mimetype="application/pdf",

            headers={

                "Content-Disposition":

                f'attachment; filename="{nome_arquivo}.pdf"'

            }

        )