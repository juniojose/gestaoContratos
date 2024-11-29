from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import UsuariosPerfisForm
from app.models import UsuariosPerfis, Status
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user
from app.middlewares import permission_required
from app.utils.log_utils import registrar_log  # Importa a função de registro de logs

usuariosperfis_bp = Blueprint('usuariosperfis', __name__, template_folder='templates')

# Lista os perfis
@usuariosperfis_bp.route("/", methods=['GET'])
@login_required
@permission_required(miniAppId=6)  # miniAppId = 6 (Gerenciamento de Perfis)
def list_usuariosPerfis():
    try:
        # Paginação
        page = request.args.get("page", 1, type=int)
        per_page = 10
        pagination = UsuariosPerfis.query.paginate(page=page, per_page=per_page, error_out=False)
        perfis = pagination.items

        # Registrar log de visualização
        registrar_log(
            miniAppId=6,
            logAcao="Visualizar Lista de Perfis de Usuários",
            logResultadoAcao=True
        )

        return render_template(
            'list_usuariosPerfis.html',
            perfis=perfis,
            pagination=pagination
        )
    except Exception as e:
        # Registrar log de falha na visualização
        registrar_log(
            miniAppId=6,
            logAcao="Tentativa de Visualizar Lista de Perfis de Usuários",
            logResultadoAcao=False
        )
        flash(f"Erro ao listar perfis: {str(e)}", "error")
        return render_template('list_usuariosPerfis.html', perfis=[], pagination=None)

# Cria um novo perfil
@usuariosperfis_bp.route("/new", methods=['GET', 'POST'])
@login_required
def new_usuariosPerfis():
    form = UsuariosPerfisForm()

    # Popula as opções do campo statusId
    form.statusId.choices = [(status.statusId, status.statusDescricao) for status in Status.query.all()]

    if form.validate_on_submit():
        try:
            # Validações específicas para evitar duplicidades
            existing_perfil = UsuariosPerfis.query.filter_by(perfilNome=form.perfilNome.data).first()
            if existing_perfil:
                flash("Erro: Já existe um perfil com esse nome.", "error")
                return render_template('usuariosPerfis_form.html', form=form, title='Cadastro de Perfil')

            # Cria o novo perfil
            perfil = UsuariosPerfis(
                perfilNome=form.perfilNome.data,
                perfilDescricao=form.perfilDescricao.data,
                statusId=form.statusId.data
            )
            db.session.add(perfil)
            db.session.commit()

            # Registrar log de criação bem-sucedida
            registrar_log(
                miniAppId=6,
                logAcao=f"Criar Perfil: {form.perfilNome.data}",
                logResultadoAcao=True
            )

            flash("Perfil cadastrado com sucesso!", "success")
            return redirect(url_for('usuariosperfis.list_usuariosPerfis'))
        except Exception as e:
            db.session.rollback()

            # Registrar log de falha na criação
            registrar_log(
                miniAppId=6,
                logAcao=f"Tentativa de Criar Perfil: {form.perfilNome.data}",
                logResultadoAcao=False
            )

            flash(f"Erro ao salvar o perfil: {str(e)}", "error")

    return render_template('usuariosPerfis_form.html', form=form, title='Cadastro de Perfil')

# Edita um perfil existente
@usuariosperfis_bp.route("/edit/<int:perfil_id>", methods=['GET', 'POST'])
@login_required
def edit_usuariosPerfis(perfil_id):
    perfil = UsuariosPerfis.query.get_or_404(perfil_id)
    form = UsuariosPerfisForm()

    # Popula as opções do campo statusId
    form.statusId.choices = [(status.statusId, status.statusDescricao) for status in Status.query.all()]

    if form.validate_on_submit():
        try:
            # Validações específicas para evitar duplicidades
            existing_perfil = UsuariosPerfis.query.filter_by(perfilNome=form.perfilNome.data).first()
            if existing_perfil and existing_perfil.perfilId != perfil_id:
                flash("Erro: Já existe outro perfil com esse nome.", "error")
                return render_template('usuariosPerfis_form.html', form=form, title='Editar Perfil')

            # Atualiza os dados do perfil
            perfil.perfilNome = form.perfilNome.data
            perfil.perfilDescricao = form.perfilDescricao.data
            perfil.statusId = form.statusId.data

            db.session.commit()

            # Registrar log de edição bem-sucedida
            registrar_log(
                miniAppId=6,
                logAcao=f"Editar Perfil: {form.perfilNome.data}",
                logResultadoAcao=True
            )

            flash("Perfil atualizado com sucesso!", "success")
            return redirect(url_for('usuariosperfis.list_usuariosPerfis'))
        except Exception as e:
            db.session.rollback()

            # Registrar log de falha na edição
            registrar_log(
                miniAppId=6,
                logAcao=f"Tentativa de Editar Perfil ID {perfil_id}",
                logResultadoAcao=False
            )

            flash(f"Erro ao atualizar o perfil: {str(e)}", "error")
    elif request.method == 'GET':
        # Preenche o formulário com os dados existentes do perfil
        form.perfilNome.data = perfil.perfilNome
        form.perfilDescricao.data = perfil.perfilDescricao
        form.statusId.data = perfil.statusId

    return render_template('usuariosPerfis_form.html', form=form, title='Editar Perfil')

# Deleta um perfil
@usuariosperfis_bp.route("/delete/<int:perfil_id>", methods=['POST'])
@login_required
def delete_usuariosPerfis(perfil_id):
    perfil = UsuariosPerfis.query.get_or_404(perfil_id)
    try:
        perfil_nome = perfil.perfilNome  # Captura o nome do perfil antes de excluir
        db.session.delete(perfil)
        db.session.commit()

        # Registrar log de exclusão bem-sucedida
        registrar_log(
            miniAppId=6,
            logAcao=f"Excluir Perfil: {perfil_nome}",
            logResultadoAcao=True
        )

        flash("Perfil deletado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()

        # Registrar log de falha na exclusão
        registrar_log(
            miniAppId=6,
            logAcao=f"Tentativa de Excluir Perfil ID {perfil_id}",
            logResultadoAcao=False
        )

        flash(f"Erro ao deletar perfil: {str(e)}", "error")
    return redirect(url_for('usuariosperfis.list_usuariosPerfis'))
