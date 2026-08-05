from app import db


class TipoServico(db.Model):
    """
    Model responsável por representar os tipos de serviço.
    """

    __tablename__ = "tipos_servico"

    id_tipo_servico = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self):

        return f"<TipoServico {self.nome}>"