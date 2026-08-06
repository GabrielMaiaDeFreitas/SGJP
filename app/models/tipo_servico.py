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

    tabelas_valores = db.relationship(

        "TabelaValores",

        back_populates="tipo_servico"

    )

    def __repr__(self):

        return f"<TipoServico {self.nome}>"