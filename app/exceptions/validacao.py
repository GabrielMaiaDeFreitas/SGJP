class ValidacaoError(Exception):
    """
    Exceção base para erros de validação
    dos dados informados pelo usuário.
    """

    def __init__(
        self,
        mensagem,
        campo=None
    ):

        super().__init__(mensagem)

        self.mensagem = mensagem

        self.campo = campo

    def __str__(self):

        return self.mensagem


class CampoObrigatorioError(
    ValidacaoError
):
    """
    Indica que um campo obrigatório
    não foi informado.
    """

    def __init__(
        self,
        campo
    ):

        super().__init__(
            f"O campo '{campo}' é obrigatório.",
            campo=campo
        )


class FormatoInvalidoError(
    ValidacaoError
):
    """
    Indica que um campo não respeita
    o formato esperado.
    """

    def __init__(
        self,
        campo,
        mensagem=None
    ):

        if mensagem is None:

            mensagem = (
                f"O campo '{campo}' "
                "possui formato inválido."
            )

        super().__init__(
            mensagem,
            campo=campo
        )


class SenhaInvalidaError(
    ValidacaoError
):
    """
    Indica que uma senha não atende
    aos critérios definidos pelo sistema.
    """

    def __init__(
        self,
        mensagem="A senha não atende aos requisitos mínimos."
    ):

        super().__init__(
            mensagem,
            campo="senha"
        )


class DocumentoInvalidoError(
    ValidacaoError
):
    """
    Indica que um documento informado
    não é válido.
    """

    def __init__(
        self,
        campo,
        mensagem=None
    ):

        if mensagem is None:

            mensagem = (
                f"O documento informado "
                f"no campo '{campo}' é inválido."
            )

        super().__init__(
            mensagem,
            campo=campo
        )


class PlacaInvalidaError(
    ValidacaoError
):
    """
    Indica que uma placa de veículo
    não está em formato válido.
    """

    def __init__(
        self,
        placa=None
    ):

        mensagem = (
            "A placa informada "
            "possui formato inválido."
        )

        if placa:

            mensagem = (
                f"A placa '{placa}' "
                "possui formato inválido."
            )

        super().__init__(
            mensagem,
            campo="placa"
        )


class DataInvalidaError(
    ValidacaoError
):
    """
    Indica que uma data não respeita
    uma regra de validação.
    """

    def __init__(
        self,
        mensagem
    ):

        super().__init__(
            mensagem,
            campo="data"
        )


class ValorInvalidoError(
    ValidacaoError
):
    """
    Indica que um valor numérico ou monetário
    não atende aos critérios definidos.
    """

    def __init__(
        self,
        campo,
        mensagem=None
    ):

        if mensagem is None:

            mensagem = (
                f"O valor informado "
                f"no campo '{campo}' é inválido."
            )

        super().__init__(
            mensagem,
            campo=campo
        )