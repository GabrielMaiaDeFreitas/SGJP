from app.exports.csv_service import CsvService
from app.exports.excel_service import ExcelService
from app.exports.pdf_service import PdfService
from app.exports.zip_service import ZipService


class ExportService:

    @staticmethod
    def exportar(
        dados,
        colunas,
        formatos,
        nome_arquivo,
        titulo,
        labels
    ):

        # Apenas um formato
        if len(formatos) == 1:

            formato = formatos[0]

            if formato == "excel":

                return ExcelService.exportar(
                    dados=dados,
                    colunas=colunas,
                    nome_arquivo=nome_arquivo,
                    titulo=titulo,
                    labels=labels
                )

            if formato == "pdf":

                return PdfService.exportar(
                    dados=dados,
                    colunas=colunas,
                    nome_arquivo=nome_arquivo,
                    titulo=titulo,
                    labels=labels
                )

            if formato == "csv":

                return CsvService.exportar(
                    dados=dados,
                    colunas=colunas,
                    nome_arquivo=nome_arquivo,
                    labels=labels
                )

            raise ValueError(
                f"Formato '{formato}' não suportado."
            )

        # Mais de um formato
        return ZipService.exportar(
            dados=dados,
            colunas=colunas,
            formatos=formatos,
            nome_arquivo=nome_arquivo,
            titulo=titulo,
            labels=labels
        )