class RegraNegocioError(Exception):
    """
    Exceção base para violações
    de regras de negócio do sistema.
    """

    def __init__(
        self,
        mensagem
    ):

        super().__init__(mensagem)

        self.mensagem = mensagem

    def __str__(self):

        return self.mensagem


class RecursoNaoEncontradoError(
    RegraNegocioError
):
    """
    Indica que o recurso solicitado
    não foi encontrado.
    """

    def __init__(
        self,
        recurso
    ):

        super().__init__(
            f"{recurso} não encontrado."
        )


class RecursoDuplicadoError(
    RegraNegocioError
):
    """
    Indica que um recurso que deveria
    ser único já existe.
    """

    def __init__(
        self,
        campo,
        valor
    ):

        super().__init__(
            f"Já existe um registro com "
            f"{campo} '{valor}'."
        )

        self.campo = campo

        self.valor = valor


class RecursoEmUsoError(
    RegraNegocioError
):
    """
    Indica que um recurso não pode ser
    removido ou alterado porque possui
    dependências no sistema.
    """

    def __init__(
        self,
        recurso,
        mensagem=None
    ):

        if mensagem is None:

            mensagem = (
                f"O {recurso} não pode ser "
                "removido porque está em uso."
            )

        super().__init__(
            mensagem
        )