from app import db


class Caminhao(db.Model):

    __tablename__ = "caminhoes"

    id_caminhao = db.Column(
        db.Integer,
        primary_key=True
    )

    placa = db.Column(
        db.String(10),
        nullable=False,
        unique=True
    )

    modelo = db.Column(
        db.String(100),
        nullable=False
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self):

        return (
            f"<Caminhao {self.placa}>"
        )