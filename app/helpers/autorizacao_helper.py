from functools import wraps

from flask import (
    flash,
    redirect,
    session,
    url_for
)


def requer_perfil(*perfis_permitidos):

    def decorator(funcao):

        @wraps(funcao)
        def wrapper(*args, **kwargs):

            if "usuario_id" not in session:

                return redirect(
                    url_for("autenticacao.login")
                )

            perfil = session.get("perfil")

            if perfil not in perfis_permitidos:

                flash(
                    "Você não tem permissão para acessar esta página.",
                    "danger"
                )

                return redirect(
                    url_for("dashboard.dashboard")
                )

            return funcao(*args, **kwargs)

        return wrapper

    return decorator


def proteger_blueprint(blueprint, *perfis_permitidos):

    @blueprint.before_request
    def verificar_perfil():

        if "usuario_id" not in session:

            return redirect(
                url_for("autenticacao.login")
            )

        perfil = session.get("perfil")

        if perfil not in perfis_permitidos:

            flash(
                "Você não tem permissão para acessar esta página.",
                "danger"
            )

            return redirect(
                url_for("dashboard.dashboard")
            )