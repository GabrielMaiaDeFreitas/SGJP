from flask import (Blueprint,redirect,render_template,session,url_for)

dashboard_bp = Blueprint("dashboard",__name__)

@dashboard_bp.route("/dashboard")
def dashboard():

    if "usuario_id" not in session:
        return redirect(url_for("autenticacao.login"))

    return render_template("dashboard/index.html")

