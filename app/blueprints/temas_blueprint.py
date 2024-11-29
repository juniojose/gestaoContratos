from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import UsuariosPreferencias
from app.forms import EscolhaTemaForm
from app import db

temas_bp = Blueprint('temas', __name__, template_folder='templates')

@temas_bp.route("/", methods=["GET", "POST"])
@login_required
def escolher_tema():
    preferencias = UsuariosPreferencias.query.filter_by(usuarioId=current_user.usuarioId).first()
    if not preferencias:
        # Cria um registro de preferência para o usuário caso não exista
        preferencias = UsuariosPreferencias(usuarioId=current_user.usuarioId, preferenciaTema='Default')
        db.session.add(preferencias)
        db.session.commit()

    form = EscolhaTemaForm(obj=preferencias)

    if form.validate_on_submit():
        preferencias.preferenciaTema = form.preferenciaTema.data
        db.session.commit()
        flash("Tema atualizado com sucesso!", "success")
        return redirect(url_for('temas.escolher_tema'))

    return render_template("escolha_tema.html", form=form, title="Escolha de Tema")
