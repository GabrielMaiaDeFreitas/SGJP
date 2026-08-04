from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Importa as models
    from app.models import Usuario

    # Importa os blueprints
    from app.routes.autenticacao_routes import autenticacao_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.usuario_routes import usuario_bp
    from app.routes.motorista_routes import motorista_bp
    from app.routes.caminhao_routes import caminhao_bp

    # Registra os blueprints
    app.register_blueprint(autenticacao_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(motorista_bp)
    app.register_blueprint(caminhao_bp)
    

    return app