from datetime import date
from decimal import Decimal

from app import db

from app.constants.atendimento import (
    VALOR_HORA_PARADA,
    VALOR_HORA_TRABALHADA,
    STATUS_OPERACIONAL_PADRAO,
    STATUS_FINANCEIRO_PADRAO
)


class Atendimento(db.Model):
    """
    Model responsável por representar os atendimentos.

    O atendimento pode ser criado de forma incompleta,
    sendo preenchido gradativamente conforme novas
    informações chegam ao operador.
    """

    __tablename__ = "atendimentos"

    id_atendimento = db.Column(
        db.Integer,
        primary_key=True
    )

    # Datas

    data_atendimento = db.Column(
        db.Date,
        nullable=True
    )

    data_cadastro = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    # Informações

    protocolo = db.Column(
        db.String(100),
        nullable=True
    )

    observacao = db.Column(
        db.Text,
        nullable=True
    )

    # Distância

    km_total = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    origem = db.Column(

        db.String(255),

        nullable=True

    )

    destino = db.Column(

        db.String(255),

        nullable=True

    )

    # Valores principais

    valor_calculado = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    valor_total = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    valor_pago = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    valor_comissao = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    # Valores adicionais

    valor_pedagio = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    valor_hora_parada = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    valor_hora_trabalhada = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    # Quantidades

    quantidade_hora_parada = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    quantidade_hora_trabalhada = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    quantidade_patins = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Flags

    cobrar_pedagio = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    cobrar_hora_parada = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    cobrar_hora_trabalhada = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    usar_patins = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # Status

    status_operacional = db.Column(
        db.String(30),
        nullable=False,
        default=STATUS_OPERACIONAL_PADRAO
    )

    status_financeiro = db.Column(
        db.String(40),
        nullable=False,
        default=STATUS_FINANCEIRO_PADRAO
    )

    # Foreign Keys

    fk_tabela_valores_id_tabela_valores = db.Column(
        db.Integer,
        db.ForeignKey(
            "tabela_valores.id_tabela_valores"
        ),
        nullable=False
    )

    fk_cliente_id_cliente = db.Column(
        db.Integer,
        db.ForeignKey(
            "clientes.id_cliente"
        ),
        nullable=True
    )

    fk_motorista_id_motorista = db.Column(
        db.Integer,
        db.ForeignKey(
            "motoristas.id_motorista"
        ),
        nullable=True
    )

    fk_caminhao_id_caminhao = db.Column(
        db.Integer,
        db.ForeignKey(
            "caminhoes.id_caminhao"
        ),
        nullable=True
    )

    fk_usuario_id_usuario = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuarios.id_usuario"
        ),
        nullable=False
    )

    # Relacionamentos

    tabela_valores = db.relationship(
        "TabelaValores",
        back_populates="atendimentos"
    )

    cliente = db.relationship(
        "Cliente",
        back_populates="atendimentos"
    )

    motorista = db.relationship(
        "Motorista",
        back_populates="atendimentos"
    )

    caminhao = db.relationship(
        "Caminhao",
        back_populates="atendimentos"
    )

    usuario = db.relationship(
        "Usuario",
        back_populates="atendimentos"
    )

    veiculo_rebocado = db.relationship(

        "VeiculoRebocado",

        back_populates="atendimento",

        uselist=False,

        cascade="all, delete-orphan"

    )

    def __repr__(self):

        return (
            f"<Atendimento {self.id_atendimento}>"
        )