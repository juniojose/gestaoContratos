from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import UsuariosPerfisForm
from app.models import UsuariosPerfis, Status  # Importe o modelo Status
from app import db
from sqlalchemy.exc import IntegrityError

usuariosperfis_bp = Blueprint('usuariosperfis', __name__, template_folder='templates')  # Nome do blueprint: 'usuariosperfis'

@usuariosperfis_bp.route("/", methods=['GET'])
def list_usuariosPerfis():
    perfis = UsuariosPerfis.query.all()
    return render_template('list_usuariosPerfis.html', perfis=perfis)

@usuariosperfis_bp.route("/new", methods=['GET', 'POST'])
def new_usuariosPerfis():
    form = UsuariosPerfisForm()

    # Popula as opções do campo statusId
    form.statusId.choices = [(status.statusId, status.statusDescricao) for status in Status.query.all()]

    if form.validate_on_submit():
        perfil = UsuariosPerfis(
            perfilNome=form.perfilNome.data,
            perfilDescricao=form.perfilDescricao.data,
            statusId=form.statusId.data
        )
        db.session.add(perfil)
        try:
            db.session.commit()
            flash('Perfil cadastrado com sucesso!', 'success')
            return redirect(url_for('usuariosperfis.list_usuariosPerfis'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe um perfil com esse nome.', 'error')
    return render_template('usuariosPerfis_form.html', form=form, title='Cadastro de Perfil')

@usuariosperfis_bp.route("/edit/<int:perfil_id>", methods=['GET', 'POST'])
def edit_usuariosPerfis(perfil_id):
    perfil = UsuariosPerfis.query.get_or_404(perfil_id)
    form = UsuariosPerfisForm()

    # Popula as opções do campo statusId
    form.statusId.choices = [(status.statusId, status.statusDescricao) for status in Status.query.all()]

    if form.validate_on_submit():
        perfil.perfilNome = form.perfilNome.data
        perfil.perfilDescricao = form.perfilDescricao.data
        perfil.statusId = form.statusId.data
        try:
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('usuariosperfis.list_usuariosPerfis'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe um perfil com esse nome.', 'error')
    elif request.method == 'GET':
        form.perfilNome.data = perfil.perfilNome
        form.perfilDescricao.data = perfil.perfilDescricao
        form.statusId.data = perfil.statusId
    return render_template('usuariosPerfis_form.html', form=form, title='Editar Perfil')

@usuariosperfis_bp.route("/delete/<int:perfil_id>", methods=['POST'])
def delete_usuariosPerfis(perfil_id):
    perfil = UsuariosPerfis.query.get_or_404(perfil_id)
    db.session.delete(perfil)
    db.session.commit()
    flash('Perfil deletado com sucesso!', 'success')
    return redirect(url_for('usuariosperfis.list_usuariosPerfis'))