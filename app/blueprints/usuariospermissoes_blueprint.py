from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import UsuariosPermissoesForm
from app.models import UsuariosPermissoes, Usuario, MiniApp, Status
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required
from app.middlewares import permission_required

usuariospermissoes_bp = Blueprint('usuariospermissoes', __name__, template_folder='templates')

@usuariospermissoes_bp.route("/", methods=["GET"])
@login_required
@permission_required(miniAppId=7)
def list_usuariosPermissoes():
    page = request.args.get("page", 1, type=int)
    try:
        permissoes = UsuariosPermissoes.query.order_by(UsuariosPermissoes.permissaoId).paginate(page=page, per_page=10, error_out=False)
    except Exception as e:
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
            flash("Permissão cadastrada com sucesso!", "success")
            return redirect(url_for('usuariospermissoes.list_usuariosPermissoes'))
        except IntegrityError:
            db.session.rollback()
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
        db.session.commit()
        flash("Permissão atualizada com sucesso!", "success")
        return redirect(url_for('usuariospermissoes.list_usuariosPermissoes'))

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
    db.session.delete(permissao)
    db.session.commit()
    flash("Permissão excluída com sucesso!", "success")
    return redirect(url_for('usuariospermissoes.list_usuariosPermissoes'))
