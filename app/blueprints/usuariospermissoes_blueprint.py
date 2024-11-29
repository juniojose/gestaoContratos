from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import UsuariosPermissoesForm
from app.models import UsuariosPermissoes, Usuario, MiniApp, Status
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user
from app.middlewares import permission_required
from app.utils.log_utils import registrar_log  # Importa a função de registro de logs

usuariospermissoes_bp = Blueprint('usuariospermissoes', __name__, template_folder='templates')

@usuariospermissoes_bp.route("/", methods=["GET"])
@login_required
@permission_required(miniAppId=7)  # miniAppId = 7 (Gerenciamento de Permissões de Usuários)
def list_usuariosPermissoes():
    page = request.args.get("page", 1, type=int)
    try:
        permissoes = UsuariosPermissoes.query.order_by(UsuariosPermissoes.permissaoId).paginate(page=page, per_page=10, error_out=False)

        # Registrar log de visualização
        registrar_log(
            miniAppId=7,
            logAcao="Visualizar Lista de Permissões de Usuários",
            logResultadoAcao=True
        )

    except Exception as e:
        # Registrar log de falha
        registrar_log(
            miniAppId=7,
            logAcao="Tentativa de Visualizar Lista de Permissões de Usuários",
            logResultadoAcao=False
        )
        flash(f"Erro ao carregar permissões: {e}", "danger")
        permissoes = None

    if permissoes:
        return render_template("list_usuariospermissoes.html", permissoes=permissoes.items, pagination=permissoes)
    else:
        return render_template("list_usuariospermissoes.html", permissoes=[], pagination=None)


@usuariospermissoes_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_usuariospermissao():
    form = UsuariosPermissoesForm()
    form.usuarioId.choices = [(u.usuarioId, u.usuarioNome) for u in Usuario.query.all()]
    form.miniAppId.choices = [(m.miniAppId, m.miniAppNome) for m in MiniApp.query.all()]
    form.statusId.choices = [(s.statusId, s.statusDescricao) for s in Status.query.all()]

    if form.validate_on_submit():
        permissao = UsuariosPermissoes(
            usuarioId=form.usuarioId.data,
            miniAppId=form.miniAppId.data,
            statusId=form.statusId.data,
            permissaoMotivo=form.permissaoMotivo.data
        )
        db.session.add(permissao)
        try:
            db.session.commit()

            # Registrar log de criação bem-sucedida
            registrar_log(
                miniAppId=7,
                logAcao=f"Criar Permissão para Usuário ID {form.usuarioId.data} e MiniApp ID {form.miniAppId.data}",
                logResultadoAcao=True
            )

            flash("Permissão cadastrada com sucesso!", "success")
            return redirect(url_for('usuariospermissoes.list_usuariosPermissoes'))
        except IntegrityError:
            db.session.rollback()

            # Registrar log de falha na criação
            registrar_log(
                miniAppId=7,
                logAcao=f"Tentativa de Criar Permissão para Usuário ID {form.usuarioId.data} e MiniApp ID {form.miniAppId.data}",
                logResultadoAcao=False
            )

            flash("Erro: Permissão já cadastrada.", "error")

    return render_template('usuariosPermissoes_form.html', form=form, title='Nova Permissão')

@usuariospermissoes_bp.route("/edit/<int:permissao_id>", methods=['GET', 'POST'])
@login_required
def edit_usuariospermissao(permissao_id):
    permissao = UsuariosPermissoes.query.get_or_404(permissao_id)
    form = UsuariosPermissoesForm()

    form.usuarioId.choices = [(u.usuarioId, u.usuarioNome) for u in Usuario.query.all()]
    form.miniAppId.choices = [(m.miniAppId, m.miniAppNome) for m in MiniApp.query.all()]
    form.statusId.choices = [(s.statusId, s.statusDescricao) for s in Status.query.all()]

    if form.validate_on_submit():
        permissao.usuarioId = form.usuarioId.data
        permissao.miniAppId = form.miniAppId.data
        permissao.statusId = form.statusId.data
        permissao.permissaoMotivo = form.permissaoMotivo.data
        try:
            db.session.commit()

            # Registrar log de edição bem-sucedida
            registrar_log(
                miniAppId=7,
                logAcao=f"Editar Permissão ID {permissao_id}",
                logResultadoAcao=True
            )

            flash("Permissão atualizada com sucesso!", "success")
            return redirect(url_for('usuariospermissoes.list_usuariosPermissoes'))
        except Exception as e:
            db.session.rollback()

            # Registrar log de falha na edição
            registrar_log(
                miniAppId=7,
                logAcao=f"Tentativa de Editar Permissão ID {permissao_id}",
                logResultadoAcao=False
            )

            flash(f"Erro ao atualizar permissão: {str(e)}", "error")
    elif request.method == 'GET':
        form.usuarioId.data = permissao.usuarioId
        form.miniAppId.data = permissao.miniAppId
        form.statusId.data = permissao.statusId
        form.permissaoMotivo.data = permissao.permissaoMotivo

    return render_template('usuariosPermissoes_form.html', form=form, title='Editar Permissão')

@usuariospermissoes_bp.route("/delete/<int:permissao_id>", methods=['POST'])
@login_required
def delete_usuariospermissao(permissao_id):
    permissao = UsuariosPermissoes.query.get_or_404(permissao_id)
    try:
        db.session.delete(permissao)
        db.session.commit()

        # Registrar log de exclusão bem-sucedida
        registrar_log(
            miniAppId=7,
            logAcao=f"Excluir Permissão ID {permissao_id}",
            logResultadoAcao=True
        )

        flash("Permissão excluída com sucesso!", "success")
    except Exception as e:
        db.session.rollback()

        # Registrar log de falha na exclusão
        registrar_log(
            miniAppId=7,
            logAcao=f"Tentativa de Excluir Permissão ID {permissao_id}",
            logResultadoAcao=False
        )

        flash(f"Erro ao excluir permissão: {str(e)}", "error")
    return redirect(url_for('usuariospermissoes.list_usuariosPermissoes'))
