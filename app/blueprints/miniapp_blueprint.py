from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import MiniAppForm
from app.models import MiniApp, Menu
from app import db
from sqlalchemy.exc import IntegrityError

miniapp_bp = Blueprint('miniapp', __name__, template_folder='templates')

# Lista os MiniApps com paginação
@miniapp_bp.route("/", methods=['GET'])
def list_miniapps():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = MiniApp.query.order_by(MiniApp.miniAppNome).paginate(page=page, per_page=per_page)
    miniapps = pagination.items
    return render_template('list_miniapps.html', miniapps=miniapps, pagination=pagination)

# Cria um novo MiniApp
@miniapp_bp.route("/new", methods=['GET', 'POST'])
def new_miniapp():
    form = MiniAppForm()
    form.menuId.choices = [(menu.menuId, menu.menuNome) for menu in Menu.query.order_by(Menu.menuNome).all()]

    if form.validate_on_submit():
        try:
            miniapp = MiniApp(
                miniAppNome=form.miniAppNome.data,
                miniAppIcon=form.miniAppIcon.data,
                menuId=form.menuId.data
            )
            db.session.add(miniapp)
            db.session.commit()
            flash("MiniApp cadastrado com sucesso!", "success")
            return redirect(url_for('miniapp.list_miniapps'))
        except IntegrityError:
            db.session.rollback()
            flash("Erro: Já existe um MiniApp com esse nome.", "error")
        except Exception as e:
            flash(f"Erro ao salvar o MiniApp: {str(e)}", "error")

    return render_template('miniapp_form.html', form=form, title="Cadastro de MiniApp")

# Edita um MiniApp existente
@miniapp_bp.route("/edit/<int:miniapp_id>", methods=['GET', 'POST'])
def edit_miniapp(miniapp_id):
    miniapp = MiniApp.query.get_or_404(miniapp_id)
    form = MiniAppForm()

    form.menuId.choices = [(menu.menuId, menu.menuNome) for menu in Menu.query.order_by(Menu.menuNome).all()]

    if form.validate_on_submit():
        try:
            miniapp.miniAppNome = form.miniAppNome.data
            miniapp.miniAppIcon = form.miniAppIcon.data
            miniapp.menuId = form.menuId.data
            db.session.commit()
            flash("MiniApp atualizado com sucesso!", "success")
            return redirect(url_for('miniapp.list_miniapps'))
        except IntegrityError:
            db.session.rollback()
            flash("Erro: Já existe um MiniApp com esse nome.", "error")
        except Exception as e:
            flash(f"Erro ao atualizar o MiniApp: {str(e)}", "error")
    elif request.method == 'GET':
        form.miniAppNome.data = miniapp.miniAppNome
        form.miniAppIcon.data = miniapp.miniAppIcon
        form.menuId.data = miniapp.menuId

    return render_template('miniapp_form.html', form=form, title="Editar MiniApp")

# Deleta um MiniApp
@miniapp_bp.route("/delete/<int:miniapp_id>", methods=['POST'])
def delete_miniapp(miniapp_id):
    miniapp = MiniApp.query.get_or_404(miniapp_id)
    try:
        db.session.delete(miniapp)
        db.session.commit()
        flash("MiniApp deletado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao deletar o MiniApp: {str(e)}", "error")

    return redirect(url_for('miniapp.list_miniapps'))
