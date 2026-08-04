from app.exports.excel_service import ExcelService
from app.exports.pdf_service import PdfService
#from app.exports.zip_service import ZipService


class ExportService:

    @staticmethod
    def exportar(
        dados,
        colunas,
        labels,
        formatos,
        nome_arquivo,
        titulo
    ):

        arquivos = []

        if "excel" in formatos:

            arquivos.append(

                ExcelService.exportar(
                    dados=dados,
                    colunas=colunas,
                    labels=labels,
                    nome_arquivo=nome_arquivo,
                    titulo=titulo
                )

            )

        if "pdf" in formatos:

            arquivos.append(

                PdfService.exportar(
                    dados=dados,
                    colunas=colunas,
                    nome_arquivo=nome_arquivo,
                    titulo=titulo
                )

            )

        #if len(arquivos) == 1:

            #return arquivos[0]

        #return ZipService.exportar(arquivos)

        if not arquivos:
            return None

        # temporário
        return arquivos[0]