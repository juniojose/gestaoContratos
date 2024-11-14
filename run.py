import os
from app import create_app

# Cria a aplicação Flask usando a fábrica de aplicações
app = create_app()

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    # Obtém o valor da variável de ambiente DEBUG, padrão é False
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']

    try:
        # Executa a aplicação Flask
        app.run(debug=debug_mode)
    except Exception as e:
        # Captura e exibe qualquer exceção que ocorra durante a execução
        print(f"Erro ao iniciar a aplicação: {e}")
