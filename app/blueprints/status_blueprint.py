from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_paginate import Pagination, get_page_args
from app.models import Status
from app.forms import StatusForm
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required
from app.middlewares import permission_required

status_bp = Blueprint('status', __name__, template_folder='templates', url_prefix='/status')

# Lista os status com paginação
@status_bp.route("/", methods=["GET"])
@login_required
@permission_required(miniAppId=4)
def list_status():
    page = request.args.get("page", 1, type=int)
    per_page = 10  # Número de itens por página
    pagination = Status.query.paginate(page=page, per_page=per_page, error_out=False)
    statuses = pagination.items  # Itens da página atual

    return render_template("list_status.html", statuses=statuses, pagination=pagination)

# Cria um novo status
@status_bp.route("/new", methods=['GET', 'POST'])
@login_required
def new_status():
    form = StatusForm()
    if form.validate_on_submit():
        status = Status(statusDescricao=form.statusDescricao.data)
        db.session.add(status)
        try:
            db.session.commit()
            flash("Status cadastrado com sucesso!", "success")
            return redirect(url_for("status.list_status"))
        except IntegrityError:
            db.session.rollback()
            flash("Erro: Já existe um status com essa descrição.", "error")
        except Exception as e:
            flash(f"Erro ao salvar o status: {str(e)}", "error")
    return render_template("status_form.html", form=form, title="Cadastro de Status")

# Edita um status existente
@status_bp.route("/edit/<int:status_id>", methods=['GET', 'POST'])
@login_required
def edit_status(status_id):
    status = Status.query.get_or_404(status_id)
    form = StatusForm()
    if form.validate_on_submit():
        existing_status = Status.query.filter_by(statusDescricao=form.statusDescricao.data).first()
        if existing_status and existing_status.statusId != status_id:
            flash("Erro: Já existe outro status com essa descrição.", "error")
        else:
            status.statusDescricao = form.statusDescricao.data
            db.session.commit()
            flash("Status atualizado com sucesso!", "success")
            return redirect(url_for("status.list_status"))
    elif request.method == "GET":
        form.statusDescricao.data = status.statusDescricao
    return render_template("status_form.html", form=form, title="Editar Status")

# Deleta um status
@status_bp.route("/delete/<int:status_id>", methods=['POST'])
@login_required
def delete_status(status_id):
    status = Status.query.get_or_404(status_id)
    try:
        db.session.delete(status)
        db.session.commit()
        flash("Status deletado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao deletar status: {str(e)}", "error")
    return redirect(url_for("status.list_status"))
