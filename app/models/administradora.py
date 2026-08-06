from app import db


class Administradora(db.Model):
    """
    Model responsável por representar as administradoras.
    """

    __tablename__ = "administradoras"

    id_administradora = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    cliente_proprio = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    clientes = db.relationship(

    "Cliente",

    back_populates="administradora"

)
    
    tabelas_valores = db.relationship(

    "TabelaValores",

    back_populates="administradora"

)

    def __repr__(self):
        """
        Representação textual do objeto.
        Facilita o debug no terminal.
        """
        return f"<Administradora {self.nome}>"