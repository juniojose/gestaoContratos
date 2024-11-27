from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import PerfisPermissoesForm
from app.models import PerfisPermissoes, UsuariosPerfis, MiniApp
from app import db
from sqlalchemy.exc import IntegrityError

perfispermissoes_bp = Blueprint('perfispermissoes', __name__, template_folder='templates')

# Listar Perfis Permissões com paginação
@perfispermissoes_bp.route("/", methods=['GET'])
def list_perfisPermissoes():
    page = request.args.get('page', 1, type=int)
    permissoes = PerfisPermissoes.query.order_by(PerfisPermissoes.perfilPermissaoId).paginate(page=page, per_page=10)
    return render_template('list_perfisPermissoes.html', permissoes=permissoes)

# Criar nova permissão
@perfispermissoes_bp.route("/new", methods=['GET', 'POST'])
def new_perfisPermissoes():
    form = PerfisPermissoesForm()

    # Popula as opções dos campos
    form.perfilId.choices = [(perfil.perfilId, perfil.perfilNome) for perfil in UsuariosPerfis.query.all()]
    form.miniAppId.choices = [(miniApp.miniAppId, miniApp.miniAppNome) for miniApp in MiniApp.query.all()]

    if form.validate_on_submit():
        permissao = PerfisPermissoes(
            perfilId=form.perfilId.data,
            miniAppId=form.miniAppId.data
        )
        db.session.add(permissao)
        try:
            db.session.commit()
            flash('Permissão criada com sucesso!', 'success')
            return redirect(url_for('perfispermissoes.list_perfisPermissoes'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe uma permissão para este perfil e miniapp.', 'error')

    return render_template('perfisPermissoes_form.html', form=form, title='Cadastro de Permissão')

# Editar permissão
@perfispermissoes_bp.route("/edit/<int:perfilPermissaoId>", methods=['GET', 'POST'])
def edit_perfisPermissoes(perfilPermissaoId):
    permissao = PerfisPermissoes.query.get_or_404(perfilPermissaoId)
    form = PerfisPermissoesForm()

    # Popula as opções dos campos
    form.perfilId.choices = [(perfil.perfilId, perfil.perfilNome) for perfil in UsuariosPerfis.query.all()]
    form.miniAppId.choices = [(miniApp.miniAppId, miniApp.miniAppNome) for miniApp in MiniApp.query.all()]

    if form.validate_on_submit():
        permissao.perfilId = form.perfilId.data
        permissao.miniAppId = form.miniAppId.data
        try:
            db.session.commit()
            flash('Permissão atualizada com sucesso!', 'success')
            return redirect(url_for('perfispermissoes.list_perfisPermissoes'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe uma permissão para este perfil e miniapp.', 'error')
    elif request.method == 'GET':
        form.perfilId.data = permissao.perfilId
        form.miniAppId.data = permissao.miniAppId

    return render_template('perfisPermissoes_form.html', form=form, title='Editar Permissão')

# Deletar permissão
@perfispermissoes_bp.route("/delete/<int:perfilPermissaoId>", methods=['POST'])
def delete_perfisPermissoes(perfilPermissaoId):
    permissao = PerfisPermissoes.query.get_or_404(perfilPermissaoId)
    try:
        db.session.delete(permissao)
        db.session.commit()
        flash('Permissão deletada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar permissão: {str(e)}', 'error')
    return redirect(url_for('perfispermissoes.list_perfisPermissoes'))
