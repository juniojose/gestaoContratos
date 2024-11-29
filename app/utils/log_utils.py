from app.models import UsuarioLog, db
from flask_login import current_user
from datetime import datetime

def registrar_log(miniAppId, logAcao, logResultadoAcao):
    """
    Registra uma ação do usuário no sistema.

    Args:
        miniAppId (int): ID do MiniApp acionado.
        logAcao (str): Descrição da ação realizada.
        logResultadoAcao (bool): Resultado da ação (True para sucesso, False para falha).
    """
    if not current_user.is_authenticated:
        return  # Evita registrar logs para usuários não autenticados

    log = UsuarioLog(
        usuarioId=current_user.usuarioId,
        miniAppId=miniAppId,
        logTimestamp=datetime.utcnow(),
        logAcao=logAcao,
        logResultadoAcao=logResultadoAcao
    )
    db.session.add(log)
    db.session.commit()
