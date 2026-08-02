from app import db


class Motorista(db.Model):
    """
    Model responsável por representar os motoristas do sistema.
    """

    __tablename__ = "motoristas"

    id_motorista = db.Column(
        db.Integer,
        primary_key=True
    )

    matricula = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    numero_cnh = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    validade_cnh = db.Column(
        db.Date,
        nullable=False
    )

    validade_toxicologico = db.Column(
        db.Date,
        nullable=False
    )

    categoria_cnh = db.Column(
        db.String(5),
        nullable=False
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self):
        return f"<Motorista {self.nome}>"