from app import create_app, db
from app.models import Status

app = create_app()

with app.app_context():
    statuses = Status.query.all()
    for status in statuses:
        print(f"ID: {status.statusId}, Descrição: {status.statusDescricao}, Data de Cadastro: {status.statusDataCadastro}, Data de Última Atualização: {status.statusDataUltimaAtualizacao}")