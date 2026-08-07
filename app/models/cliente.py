from app import db


class Cliente(db.Model):
    """
    Model responsável por representar os clientes.
    """

    __tablename__ = "clientes"

    id_cliente = db.Column(
        db.Integer,
        primary_key=True
    )

    nome_fantasia = db.Column(
        db.String(100),
        nullable=False
    )

    cnpj = db.Column(
        db.String(18),
        nullable=False,
        unique=True
    )

    razao_social = db.Column(
        db.String(150),
        nullable=False
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    fk_administradora_id_administradora = db.Column(
        db.Integer,
        db.ForeignKey(
            "administradoras.id_administradora"
        ),
        nullable=False
    )

    administradora = db.relationship(
        "Administradora",
        back_populates="clientes"
    )

    atendimentos = db.relationship(
        "Atendimento",
        back_populates="cliente"
    )

    def __repr__(self):

        return f"<Cliente {self.nome_fantasia}>"