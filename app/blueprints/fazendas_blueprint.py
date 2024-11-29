from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import FazendaForm
from app.models import Fazenda, Status
from app import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required
from app.middlewares import permission_required
from app.utils.log_utils import registrar_log  # Importa a função de logs

fazendas_bp = Blueprint('fazendas', __name__, template_folder='templates')

@fazendas_bp.route("/", methods=["GET"])
@login_required
@permission_required(miniAppId=1)
def list_fazendas():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    pagination = Fazenda.query.paginate(page=page, per_page=per_page, error_out=False)
    fazendas = pagination.items

    # Registrar log de visualização da lista de fazendas
    registrar_log(miniAppId=1, logAcao="Listar Fazendas", logResultadoAcao=True)

    return render_template("list_fazendas.html", fazendas=fazendas, pagination=pagination)

@fazendas_bp.route("/new", methods=['GET', 'POST'])
@login_required
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

            # Registrar log de sucesso ao criar uma fazenda
            registrar_log(miniAppId=1, logAcao="Criar Fazenda", logResultadoAcao=True)

            return redirect(url_for('fazendas.list_fazendas'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe uma fazenda com essa sigla ou nome.', 'error')

            # Registrar log de falha ao criar uma fazenda
            registrar_log(miniAppId=1, logAcao="Criar Fazenda", logResultadoAcao=False)
    return render_template('fazenda_form.html', form=form, title='Cadastro de Fazenda')

@fazendas_bp.route("/edit/<int:fazenda_id>", methods=['GET', 'POST'])
@login_required
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

            # Registrar log de sucesso ao editar uma fazenda
            registrar_log(miniAppId=1, logAcao=f"Editar Fazenda ID {fazenda_id}", logResultadoAcao=True)

            return redirect(url_for('fazendas.list_fazendas'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Já existe uma fazenda com essa sigla ou nome.', 'error')

            # Registrar log de falha ao editar uma fazenda
            registrar_log(miniAppId=1, logAcao=f"Editar Fazenda ID {fazenda_id}", logResultadoAcao=False)
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

@fazendas_bp.route("/delete/<int:fazenda_id>", methods=['POST'])
@login_required
def delete_fazenda(fazenda_id):
    fazenda = Fazenda.query.get_or_404(fazenda_id)
    try:
        db.session.delete(fazenda)
        db.session.commit()
        flash('Fazenda deletada com sucesso!', 'success')

        # Registrar log de sucesso ao deletar uma fazenda
        registrar_log(miniAppId=1, logAcao=f"Deletar Fazenda ID {fazenda_id}", logResultadoAcao=True)
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar fazenda: {str(e)}', 'error')

        # Registrar log de falha ao deletar uma fazenda
        registrar_log(miniAppId=1, logAcao=f"Deletar Fazenda ID {fazenda_id}", logResultadoAcao=False)

    return redirect(url_for('fazendas.list_fazendas'))
