from flask import Blueprint, render_template, request
from app.models import UsuarioLog
from flask_login import login_required

logs_bp = Blueprint('logs', __name__, template_folder='templates')

@logs_bp.route("/", methods=["GET"])
@login_required
def list_logs():
    page = request.args.get("page", 1, type=int)
    logs = UsuarioLog.query.order_by(UsuarioLog.logTimestamp.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template("list_logs.html", logs=logs.items, pagination=logs)
