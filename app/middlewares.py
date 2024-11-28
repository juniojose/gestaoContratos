from flask import abort, flash, redirect, url_for
from flask_login import current_user

def has_permission(miniAppId):
    """
    Verifica se o usuário tem permissão para acessar um miniApp.
    """
    if not current_user.is_authenticated:
        return False

    # Verifica permissões do perfil
    for permissao in current_user.perfil.perfisPermissoes:
        if permissao.miniAppId == miniAppId:
            return True

    # Verifica permissões diretas do usuário
    for permissao in current_user.usuariosPermissoes:
        if permissao.miniAppId == miniAppId:
            return True

    return False

def permission_required(miniAppId):
    """
    Decorador para proteger uma rota com base em permissões.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not has_permission(miniAppId):
                flash("Você não tem permissão para acessar este recurso.", "danger")
                return redirect(url_for('main_bp.home'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
