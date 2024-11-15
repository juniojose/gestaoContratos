from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import StatusForm
from .models import Status
from app import db
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)

# Rota para login
@main.route("/", methods=['GET', 'POST'])
def login():
    return redirect(url_for('main.home'))

# Rota para a página inicial
@main.route("/home")
def home():
    return render_template('home.html')

# Rota para listar todos os status
@main.route("/status", methods=['GET'])
def list_status():
    statuses = Status.query.all()
    return render_template('list_status.html', statuses=statuses)

# Rota para criar um novo status
@main.route("/status/new", methods=['GET', 'POST'])
def new_status():
    form = StatusForm()
    if form.validate_on_submit():
        status = Status(
            statusDescricao=form.statusDescricao.data
        )
        db.session.add(status)
        try:
            db.session.commit()
            flash('Status cadastrado com sucesso!', 'success')
            return redirect(url_for('main.list_status'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe um status com essa descrição.', 'error')
            return redirect(url_for('main.new_status'))
    return render_template('status_form.html', form=form, title='Novo Status')

# Rota para editar um status existente
@main.route("/status/edit/<int:status_id>", methods=['GET', 'POST'])
def edit_status(status_id):
    status = Status.query.get_or_404(status_id)
    form = StatusForm()
    if form.validate_on_submit():
        # Verificar se o novo status já existe (exceto para o próprio registro que está sendo editado)
        existing_status = Status.query.filter_by(statusDescricao=form.statusDescricao.data).first()
        if existing_status and existing_status.statusId != status_id:
            flash('Erro: Já existe outro status com essa descrição.', 'error')
            return redirect(url_for('main.edit_status', status_id=status_id))

        status.statusDescricao = form.statusDescricao.data
        try:
            db.session.commit()
            flash('Status atualizado com sucesso!', 'success')
            return redirect(url_for('main.list_status'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Não foi possível atualizar o status devido a uma violação de restrição.', 'error')
            return redirect(url_for('main.edit_status', status_id=status_id))
    elif request.method == 'GET':
        form.statusDescricao.data = status.statusDescricao
    return render_template('status_form.html', form=form, title='Editar Status')

# Rota para deletar um status
@main.route("/status/delete/<int:status_id>", methods=['POST'])
def delete_status(status_id):
    status = Status.query.get_or_404(status_id)
    db.session.delete(status)
    db.session.commit()
    flash('Status deletado com sucesso!', 'success')
    return redirect(url_for('main.list_status'))
