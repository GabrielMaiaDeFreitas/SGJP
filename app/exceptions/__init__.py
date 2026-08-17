from app.exceptions.validacao import (
    ValidacaoError,
    CampoObrigatorioError,
    FormatoInvalidoError,
    SenhaInvalidaError,
    DocumentoInvalidoError,
    PlacaInvalidaError,
    DataInvalidaError,
    ValorInvalidoError
)

from app.exceptions.negocio import (
    RegraNegocioError,
    RecursoNaoEncontradoError,
    RecursoDuplicadoError,
    RecursoEmUsoError
)