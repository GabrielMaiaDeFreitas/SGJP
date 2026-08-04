from flask import (
    flash,
    redirect
)


class PdfService:

    @staticmethod
    def exportar(
        dados,
        colunas,
        nome_arquivo,
        url_retorno
    ):

        flash(
            "Exportação em PDF será implementada em breve.",
            "info"
        )

        return redirect(
            url_retorno
        )