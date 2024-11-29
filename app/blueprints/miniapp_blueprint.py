from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import MiniAppForm
from app.models import MiniApp, Menu
from app import db
from flask_login import login_required, current_user
from app.utils.log_utils import registrar_log  # Importa a função de registro de logs

# Definindo o blueprint com o nome correto
miniapps_bp = Blueprint('miniapp', __name__, template_folder='templates')

@miniapps_bp.route("/", methods=["GET"])
@login_required
def list_miniapps():
    page = request.args.get("page", 1, type=int)
    miniapps = MiniApp.query.paginate(page=page, per_page=10, error_out=False)

    # Registrar log de visualização da lista de MiniApps
    registrar_log(
        miniAppId=None,
        logAcao="Visualizar Lista de MiniApps",
        logResultadoAcao=True
    )

    return render_template("list_miniapps.html", miniapps=miniapps.items, pagination=miniapps)

@miniapps_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_miniapp():
    form = MiniAppForm()
    if form.validate_on_submit():
        miniapp = MiniApp(
            miniAppNome=form.miniAppNome.data,
            miniAppIcon=form.miniAppIcon.data,
            miniAppLink=form.miniAppLink.data,
            menuId=form.menuId.data.menuId  # Obter o ID do menu selecionado
        )
        db.session.add(miniapp)
        try:
            db.session.commit()

            # Registrar log de criação de MiniApp
            registrar_log(
                miniAppId=miniapp.miniAppId,
                logAcao=f"Criar MiniApp: {miniapp.miniAppNome}",
                logResultadoAcao=True
            )

            flash("MiniApp criado com sucesso!", "success")
            return redirect(url_for("miniapp.list_miniapps"))
        except Exception as e:
            db.session.rollback()

            # Registrar log de falha na criação de MiniApp
            registrar_log(
                miniAppId=None,
                logAcao="Tentativa de Criar MiniApp",
                logResultadoAcao=False
            )
            flash(f"Erro ao criar o MiniApp: {str(e)}", "danger")

    return render_template("miniapp_form.html", form=form, title="Novo MiniApp")

@miniapps_bp.route("/edit/<int:miniapp_id>", methods=["GET", "POST"])
@login_required
def edit_miniapp(miniapp_id):
    miniapp = MiniApp.query.get_or_404(miniapp_id)
    form = MiniAppForm(obj=miniapp)
    if form.validate_on_submit():
        miniapp.miniAppNome = form.miniAppNome.data
        miniapp.miniAppIcon = form.miniAppIcon.data
        miniapp.miniAppLink = form.miniAppLink.data
        miniapp.menuId = form.menuId.data.menuId  # Obter o ID do menu selecionado

        try:
            db.session.commit()

            # Registrar log de edição de MiniApp
            registrar_log(
                miniAppId=miniapp.miniAppId,
                logAcao=f"Editar MiniApp: {miniapp.miniAppNome}",
                logResultadoAcao=True
            )

            flash("MiniApp atualizado com sucesso!", "success")
            return redirect(url_for("miniapp.list_miniapps"))
        except Exception as e:
            db.session.rollback()

            # Registrar log de falha na edição de MiniApp
            registrar_log(
                miniAppId=miniapp.miniAppId,
                logAcao=f"Tentativa de Editar MiniApp: {miniapp.miniAppNome}",
                logResultadoAcao=False
            )

            flash(f"Erro ao atualizar o MiniApp: {str(e)}", "danger")

    return render_template("miniapp_form.html", form=form, title="Editar MiniApp")

@miniapps_bp.route("/delete/<int:miniapp_id>", methods=["POST"])
@login_required
def delete_miniapp(miniapp_id):
    miniapp = MiniApp.query.get_or_404(miniapp_id)
    try:
        db.session.delete(miniapp)
        db.session.commit()

        # Registrar log de exclusão de MiniApp
        registrar_log(
            miniAppId=miniapp.miniAppId,
            logAcao=f"Excluir MiniApp: {miniapp.miniAppNome}",
            logResultadoAcao=True
        )

        flash("MiniApp excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()

        # Registrar log de falha na exclusão de MiniApp
        registrar_log(
            miniAppId=miniapp.miniAppId,
            logAcao=f"Tentativa de Excluir MiniApp: {miniapp.miniAppNome}",
            logResultadoAcao=False
        )

        flash(f"Erro ao excluir o MiniApp: {str(e)}", "danger")

    return redirect(url_for("miniapp.list_miniapps"))
