from app import db


class VeiculoRebocado(db.Model):

    __tablename__ = "veiculos_rebocados"

    fk_atendimento_id_atendimento = db.Column(

        db.Integer,

        db.ForeignKey(

            "atendimentos.id_atendimento"

        ),

        primary_key=True

    )

    placa = db.Column(

        db.String(10),

        nullable=True

    )

    modelo = db.Column(

        db.String(100),

        nullable=True

    )

    atendimento = db.relationship(

        "Atendimento",

        back_populates="veiculo_rebocado"

    )