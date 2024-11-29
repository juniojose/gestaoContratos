from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import MiniAppForm
from app.models import MiniApp, Menu
from app import db
from flask_login import login_required

# Definindo o blueprint com o nome correto
miniapps_bp = Blueprint('miniapp', __name__, template_folder='templates')

@miniapps_bp.route("/", methods=["GET"])
@login_required
def list_miniapps():
    page = request.args.get("page", 1, type=int)
    miniapps = MiniApp.query.paginate(page=page, per_page=10, error_out=False)
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
        db.session.commit()
        flash("MiniApp criado com sucesso!", "success")
        return redirect(url_for("miniapp.list_miniapps"))
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
        db.session.commit()
        flash("MiniApp atualizado com sucesso!", "success")
        return redirect(url_for("miniapp.list_miniapps"))
    return render_template("miniapp_form.html", form=form, title="Editar MiniApp")

@miniapps_bp.route("/delete/<int:miniapp_id>", methods=["POST"])
@login_required
def delete_miniapp(miniapp_id):
    miniapp = MiniApp.query.get_or_404(miniapp_id)
    db.session.delete(miniapp)
    db.session.commit()
    flash("MiniApp excluído com sucesso!", "success")
    return redirect(url_for("miniapp.list_miniapps"))
