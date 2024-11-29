from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import EscolherMiniAppsHomeForm
from app.models import MiniApp, UsuariosPreferencias
from app import db

preferencias_bp = Blueprint('preferencias', __name__, template_folder='templates')

@preferencias_bp.route("/miniapps_home", methods=["GET", "POST"])
@login_required
def escolher_miniapps_home():
    # Recuperar os MiniApps que o usuário tem permissão
    miniapps_permitidos = [
        permissao.miniApp for permissao in current_user.perfil.perfisPermissoes
    ] + [
        permissao.miniApp for permissao in current_user.usuariosPermissoes
    ]

    # Remover duplicados
    miniapps_permitidos = {miniapp.miniAppId: miniapp for miniapp in miniapps_permitidos}.values()

    # Recuperar preferências do usuário
    preferencias = UsuariosPreferencias.query.filter_by(usuarioId=current_user.usuarioId).first()

    # Inicializar o formulário
    form = EscolherMiniAppsHomeForm()
    form.miniapps.choices = [(miniapp.miniAppId, miniapp.miniAppNome) for miniapp in miniapps_permitidos]

    if request.method == 'GET' and preferencias:
        # Preencher o formulário com os MiniApps já selecionados
        form.miniapps.data = preferencias.preferenciaMiniAppsHome or []

    if form.validate_on_submit():
        # Atualizar ou criar as preferências do usuário
        if not preferencias:
            preferencias = UsuariosPreferencias(usuarioId=current_user.usuarioId)
            db.session.add(preferencias)

        preferencias.preferenciaMiniAppsHome = form.miniapps.data
        db.session.commit()
        flash("Preferências de MiniApps salvas com sucesso!", "success")
        return redirect(url_for('main_bp.home'))

    return render_template('escolher_miniapps_home.html', form=form, title="Escolher MiniApps da Home")
