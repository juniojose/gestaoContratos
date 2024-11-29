from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import PerfisPermissoesForm
from app.models import PerfisPermissoes, UsuariosPerfis, MiniApp
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user
from app.middlewares import permission_required
from app.utils.log_utils import registrar_log  # Importa a função de registro de logs

perfispermissoes_bp = Blueprint('perfispermissoes', __name__, template_folder='templates')

# Listar Perfis Permissões com paginação
@perfispermissoes_bp.route("/", methods=['GET'])
@login_required
@permission_required(miniAppId=1)
def list_perfisPermissoes():
    page = request.args.get('page', 1, type=int)
    permissoes = PerfisPermissoes.query.order_by(PerfisPermissoes.perfilPermissaoId).paginate(page=page, per_page=10)

    # Registrar log de visualização da lista de permissões
    registrar_log(
        miniAppId=1,  # Supondo que o MiniApp com ID 1 é o responsável por listar permissões
        logAcao="Visualizar Lista de PerfisPermissoes",
        logResultadoAcao=True
    )

    return render_template('list_perfisPermissoes.html', permissoes=permissoes)

# Criar nova permissão
@perfispermissoes_bp.route("/new", methods=['GET', 'POST'])
@login_required
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

            # Registrar log de criação de permissão
            registrar_log(
                miniAppId=1,  # ID do MiniApp responsável pela funcionalidade de permissões
                logAcao=f"Criar Permissão para Perfil {form.perfilId.data} e MiniApp {form.miniAppId.data}",
                logResultadoAcao=True
            )

            flash('Permissão criada com sucesso!', 'success')
            return redirect(url_for('perfispermissoes.list_perfisPermissoes'))
        except IntegrityError:
            db.session.rollback()

            # Registrar log de falha na criação de permissão
            registrar_log(
                miniAppId=1,
                logAcao="Tentativa de Criar Permissão",
                logResultadoAcao=False
            )

            flash('Erro: Já existe uma permissão para este perfil e miniapp.', 'error')

    return render_template('perfisPermissoes_form.html', form=form, title='Cadastro de Permissão')

# Editar permissão
@perfispermissoes_bp.route("/edit/<int:perfilPermissaoId>", methods=['GET', 'POST'])
@login_required
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

            # Registrar log de edição de permissão
            registrar_log(
                miniAppId=1,
                logAcao=f"Editar Permissão ID {perfilPermissaoId} para Perfil {form.perfilId.data} e MiniApp {form.miniAppId.data}",
                logResultadoAcao=True
            )

            flash('Permissão atualizada com sucesso!', 'success')
            return redirect(url_for('perfispermissoes.list_perfisPermissoes'))
        except IntegrityError:
            db.session.rollback()

            # Registrar log de falha na edição de permissão
            registrar_log(
                miniAppId=1,
                logAcao=f"Tentativa de Editar Permissão ID {perfilPermissaoId}",
                logResultadoAcao=False
            )

            flash('Erro: Já existe uma permissão para este perfil e miniapp.', 'error')
    elif request.method == 'GET':
        form.perfilId.data = permissao.perfilId
        form.miniAppId.data = permissao.miniAppId

    return render_template('perfisPermissoes_form.html', form=form, title='Editar Permissão')

# Deletar permissão
@perfispermissoes_bp.route("/delete/<int:perfilPermissaoId>", methods=['POST'])
@login_required
def delete_perfisPermissoes(perfilPermissaoId):
    permissao = PerfisPermissoes.query.get_or_404(perfilPermissaoId)
    try:
        db.session.delete(permissao)
        db.session.commit()

        # Registrar log de exclusão de permissão
        registrar_log(
            miniAppId=1,
            logAcao=f"Excluir Permissão ID {perfilPermissaoId}",
            logResultadoAcao=True
        )

        flash('Permissão deletada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()

        # Registrar log de falha na exclusão de permissão
        registrar_log(
            miniAppId=1,
            logAcao=f"Tentativa de Excluir Permissão ID {perfilPermissaoId}",
            logResultadoAcao=False
        )

        flash(f'Erro ao deletar permissão: {str(e)}', 'error')

    return redirect(url_for('perfispermissoes.list_perfisPermissoes'))
