from app import db
from werkzeug.security import (generate_password_hash,check_password_hash)

class Usuario(db.Model):
    """
    Model responsável por representar os usuários do sistema.
    """

    __tablename__ = "usuarios"

    id_usuario = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    login = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )

    perfil = db.Column(
        db.String(30),
        nullable=False
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self):
        """
        Representação textual do objeto.
        Facilita o debug no terminal.
        """
        return f"<Usuario {self.nome}>"

    def set_senha(self, senha):
        """
        Gera o hash da senha antes de armazená-la.
        """
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        """
        Verifica se a senha informada corresponde ao hash armazenado.
        """
        return check_password_hash(self.senha, senha)