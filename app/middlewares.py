from flask import abort, flash, redirect, url_for
from flask_login import current_user

def has_permission(miniAppId):
    """
    Verifica se o usuário autenticado tem permissão para acessar um miniApp específico.
    """
    if not current_user.is_authenticated:
        return False

    # Verifica as permissões do perfil do usuário autenticado
    for permissao in current_user.perfil.perfisPermissoes:
        if permissao.miniAppId == miniAppId:
            return True
    return False

def permission_required(miniAppId):
    """
    Decorador para proteger uma rota com base em permissões do miniApp.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not has_permission(miniAppId):
                # Redireciona para a página de erro personalizada
                flash("Você não tem permissão para acessar este recurso.", "danger")
                return abort(403)
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__  # Preserva o nome original da função
        return wrapper
    return decorator
