import os
from app import create_app, db
from app.models import Usuario

app = create_app()

with app.app_context():

    usuario = Usuario.query.filter_by(login="admin").first()

    if usuario is None:

        administrador = Usuario(
            nome="Administrador",
            login="admin",
            perfil="Administrador",
            ativo=True
        )

        administrador.set_senha(os.getenv("ADMIN_PASSWORD"))

        db.session.add(administrador)

        db.session.commit()

        print("Administrador criado com sucesso!")

    else:

        print("Administrador já existe.")