from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import StatusForm, FazendaForm, UsuariosPerfisForm
from .models import Status, Fazenda, UsuariosPerfis
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
    return render_template('status_form.html', form=form, title='Cadastro de Status')

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

@main.route('/debug/fazendas')
def debug_fazendas():
    fazendas = Fazenda.query.all()
    return "<br>".join([f"{f.fazendaId} - {f.fazendaNome} - {f.statusId}" for f in fazendas])

@main.route("/fazendas", methods=['GET'])
def list_fazendas():
    fazendas = Fazenda.query.all()
    return render_template('list_fazendas.html', fazendas=fazendas)

@main.route("/fazendas/new", methods=['GET', 'POST'])
def new_fazenda():
    form = FazendaForm()

    # Carregar as opções de Status do banco de dados
    form.statusId.choices = [(status.statusId, status.statusDescricao) for status in Status.query.all()]

    if form.validate_on_submit():
        fazenda = Fazenda(
            fazendaSigla=form.fazendaSigla.data,
            fazendaNome=form.fazendaNome.data,
            fazendaCEP=form.fazendaCEP.data,
            fazendaEstado=form.fazendaEstado.data,
            fazendaCidade=form.fazendaCidade.data,
            fazendaBairro=form.fazendaBairro.data,
            fazendaLogradouro=form.fazendaLogradouro.data,
            fazendaNumero=form.fazendaNumero.data,
            fazendaComplemento=form.fazendaComplemento.data,
            statusId=form.statusId.data
        )
        db.session.add(fazenda)
        try:
            db.session.commit()
            flash('Fazenda cadastrada com sucesso!', 'success')
            return redirect(url_for('main.list_fazendas'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe uma fazenda com essa sigla ou nome.', 'error')
    return render_template('fazenda_form.html', form=form, title='Cadastro de Fazenda')

@main.route("/fazendas/edit/<int:fazenda_id>", methods=['GET', 'POST'])
def edit_fazenda(fazenda_id):
    fazenda = Fazenda.query.get_or_404(fazenda_id)
    form = FazendaForm(fazenda_id=fazenda_id)

    # Popula as opções do campo statusId
    form.statusId.choices = [(status.statusId, status.statusDescricao) for status in Status.query.all()]

    if form.validate_on_submit():
        fazenda.fazendaSigla = form.fazendaSigla.data
        fazenda.fazendaNome = form.fazendaNome.data
        fazenda.fazendaCEP = form.fazendaCEP.data
        fazenda.fazendaEstado = form.fazendaEstado.data
        fazenda.fazendaCidade = form.fazendaCidade.data
        fazenda.fazendaBairro = form.fazendaBairro.data
        fazenda.fazendaLogradouro = form.fazendaLogradouro.data
        fazenda.fazendaNumero = form.fazendaNumero.data
        fazenda.fazendaComplemento = form.fazendaComplemento.data
        fazenda.statusId = form.statusId.data

        try:
            db.session.commit()
            flash('Fazenda atualizada com sucesso!', 'success')
            return redirect(url_for('main.list_fazendas'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe uma fazenda com essa sigla ou nome.', 'error')
    elif request.method == 'GET':
        form.fazendaSigla.data = fazenda.fazendaSigla
        form.fazendaNome.data = fazenda.fazendaNome
        form.fazendaCEP.data = fazenda.fazendaCEP
        form.fazendaEstado.data = fazenda.fazendaEstado
        form.fazendaCidade.data = fazenda.fazendaCidade
        form.fazendaBairro.data = fazenda.fazendaBairro
        form.fazendaLogradouro.data = fazenda.fazendaLogradouro
        form.fazendaNumero.data = fazenda.fazendaNumero
        form.fazendaComplemento.data = fazenda.fazendaComplemento
        form.statusId.data = fazenda.statusId

    return render_template('fazenda_form.html', form=form, title='Editar Fazenda')

@main.route("/fazendas/delete/<int:fazenda_id>", methods=['POST'])
def delete_fazenda(fazenda_id):
    fazenda = Fazenda.query.get_or_404(fazenda_id)
    db.session.delete(fazenda)
    db.session.commit()
    flash('Fazenda deletada com sucesso!', 'success')
    return redirect(url_for('main.list_fazendas'))

@main.route("/usuariosPerfis", methods=['GET'])
def list_usuariosPerfis():
    perfis = UsuariosPerfis.query.all()
    return render_template('list_usuariosPerfis.html', perfis=perfis)

@main.route("/usuariosPerfis/new", methods=['GET', 'POST'])
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
            return redirect(url_for('main.list_usuariosPerfis'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe um perfil com esse nome.', 'error')
    return render_template('usuariosPerfis_form.html', form=form, title='Cadastro de Perfil')

@main.route("/usuariosPerfis/edit/<int:perfil_id>", methods=['GET', 'POST'])
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
            return redirect(url_for('main.list_usuariosPerfis'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe um perfil com esse nome.', 'error')
    elif request.method == 'GET':
        form.perfilNome.data = perfil.perfilNome
        form.perfilDescricao.data = perfil.perfilDescricao
        form.statusId.data = perfil.statusId
    return render_template('usuariosPerfis_form.html', form=form, title='Editar Perfil')

@main.route("/usuariosPerfis/delete/<int:perfil_id>", methods=['POST'])
def delete_usuariosPerfis(perfil_id):
    perfil = UsuariosPerfis.query.get_or_404(perfil_id)
    db.session.delete(perfil)
    db.session.commit()
    flash('Perfil deletado com sucesso!', 'success')
    return redirect(url_for('main.list_usuariosPerfis'))
