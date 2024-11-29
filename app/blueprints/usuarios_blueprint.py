from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import UsuarioForm
from app.models import Usuario, Status, Fazenda, UsuariosPerfis
from app import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user
from app.middlewares import permission_required
from app.utils.log_utils import registrar_log  # Importa a função de registro de logs

usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')

@usuarios_bp.route("/", methods=["GET"])
@login_required
@permission_required(miniAppId=5)  # miniAppId = 5 (Gerenciamento de Usuários)
def list_usuarios():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    pagination = Usuario.query.paginate(page=page, per_page=per_page, error_out=False)
    usuarios = pagination.items

    # Registrar log de visualização
    registrar_log(
        miniAppId=5,
        logAcao="Visualizar Lista de Usuários",
        logResultadoAcao=True
    )

    return render_template("list_usuarios.html", usuarios=usuarios, pagination=pagination)

@usuarios_bp.route("/new", methods=['GET', 'POST'])
@login_required
def new_usuario():
    form = UsuarioForm()

    form.statusId.choices = [(status.statusId, status.statusDescricao) for status in Status.query.all()]
    form.fazendaId.choices = [(fazenda.fazendaId, fazenda.fazendaNome) for fazenda in Fazenda.query.all()]
    form.usuarioPerfilId.choices = [(perfil.perfilId, perfil.perfilNome) for perfil in UsuariosPerfis.query.all()]

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.usuarioSenha.data).decode('utf-8')
        usuario = Usuario(
            usuarioNome=form.usuarioNome.data,
            usuarioEmail=form.usuarioEmail.data,
            usuarioSenha=hashed_password,
            usuarioDataValidadePermissao=form.usuarioDataValidadePermissao.data,
            statusId=form.statusId.data,
            fazendaId=form.fazendaId.data if form.fazendaId.data != -1 else None,
            usuarioPerfilId=form.usuarioPerfilId.data
        )
        db.session.add(usuario)
        try:
            db.session.commit()

            # Registrar log de criação bem-sucedida
            registrar_log(
                miniAppId=5,
                logAcao=f"Criar Usuário: {form.usuarioEmail.data}",
                logResultadoAcao=True
            )

            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('usuarios.list_usuarios'))
        except IntegrityError:
            db.session.rollback()

            # Registrar log de falha na criação
            registrar_log(
                miniAppId=5,
                logAcao=f"Tentativa de Criar Usuário: {form.usuarioEmail.data}",
                logResultadoAcao=False
            )

            flash('Erro: Já existe um usuário com este e-mail.', 'error')

    return render_template('usuario_form.html', form=form, title='Cadastro de Usuário')

@usuarios_bp.route("/edit/<int:usuario_id>", methods=['GET', 'POST'])
@login_required
def edit_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    form = UsuarioForm(usuario_id=usuario_id)

    form.statusId.choices = [(status.statusId, status.statusDescricao) for status in Status.query.all()]
    form.fazendaId.choices = [(-1, 'Nenhuma')] + [(fazenda.fazendaId, fazenda.fazendaNome) for fazenda in Fazenda.query.all()]
    form.usuarioPerfilId.choices = [(perfil.perfilId, perfil.perfilNome) for perfil in UsuariosPerfis.query.all()]

    if form.validate_on_submit():
        if form.usuarioSenha.data:
            usuario.usuarioSenha = bcrypt.generate_password_hash(form.usuarioSenha.data).decode('utf-8')
        usuario.usuarioNome = form.usuarioNome.data
        usuario.usuarioEmail = form.usuarioEmail.data
        usuario.usuarioDataValidadePermissao = form.usuarioDataValidadePermissao.data
        usuario.statusId = form.statusId.data
        usuario.fazendaId = form.fazendaId.data if form.fazendaId.data != -1 else None
        usuario.usuarioPerfilId = form.usuarioPerfilId.data
        try:
            db.session.commit()

            # Registrar log de edição bem-sucedida
            registrar_log(
                miniAppId=5,
                logAcao=f"Editar Usuário: {form.usuarioEmail.data}",
                logResultadoAcao=True
            )

            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('usuarios.list_usuarios'))
        except IntegrityError:
            db.session.rollback()

            # Registrar log de falha na edição
            registrar_log(
                miniAppId=5,
                logAcao=f"Tentativa de Editar Usuário: {form.usuarioEmail.data}",
                logResultadoAcao=False
            )

            flash('Erro: Não foi possível atualizar o usuário.', 'error')
    elif request.method == 'GET':
        form.usuarioNome.data = usuario.usuarioNome
        form.usuarioEmail.data = usuario.usuarioEmail
        form.usuarioSenha.data = ''  # Evita preencher o campo de senha
        form.usuarioDataValidadePermissao.data = usuario.usuarioDataValidadePermissao
        form.statusId.data = usuario.statusId
        form.fazendaId.data = usuario.fazendaId if usuario.fazendaId else -1
        form.usuarioPerfilId.data = usuario.usuarioPerfilId

    return render_template('usuario_form.html', form=form, title='Editar Usuário')

@usuarios_bp.route("/delete/<int:usuario_id>", methods=['POST'])
@login_required
def delete_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    try:
        usuario_email = usuario.usuarioEmail  # Captura o e-mail do usuário antes de excluir
        db.session.delete(usuario)
        db.session.commit()

        # Registrar log de exclusão bem-sucedida
        registrar_log(
            miniAppId=5,
            logAcao=f"Excluir Usuário: {usuario_email}",
            logResultadoAcao=True
        )

        flash('Usuário deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()

        # Registrar log de falha na exclusão
        registrar_log(
            miniAppId=5,
            logAcao=f"Tentativa de Excluir Usuário ID {usuario_id}",
            logResultadoAcao=False
        )

        flash(f'Erro ao deletar usuário: {str(e)}', 'error')
    return redirect(url_for('usuarios.list_usuarios'))
