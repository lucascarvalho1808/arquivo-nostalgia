from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from routes.extensions import supabase  

# Blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.filmes import filmes_bp
from routes.series import series_bp
from routes.jogos import jogos_bp
from routes.busca import busca_bp  
from routes.listas import listas_bp
from routes.detalhes import detalhes_bp
from routes.arquivos import arquivos_bp
from routes.perfil import perfil_bp
from services.agendador_ranking import agendador

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Criação da instância principal do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

# Configuração do gerenciador de login do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 
login_manager.login_message = "Faça login para continuar." 
login_manager.login_message_category = "info" 

@login_manager.user_loader
def load_user(user_id):
    """
    Função para carregar o usuário logado a partir do ID salvo na sessão.
    Busca informações do usuário autenticado no Supabase.
    """
    try:
        user_response = supabase.auth.get_user()
        if user_response and user_response.user and user_response.user.id == user_id:
            user_data = user_response.user
            profile_data = supabase.table("profiles").select("*").eq("id", user_data.id).single().execute().data
            username = profile_data["username"] if profile_data else 'Usuário'
            return User(
                id=user_data.id,
                email=user_data.email,
                username=username,
                created_at=profile_data.get("created_at") if profile_data else None
            )
    except Exception as e:
        print(f"Erro ao carregar usuário da sessão: {e}")
    return None

# Registro dos Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(filmes_bp)
app.register_blueprint(series_bp)
app.register_blueprint(jogos_bp)
app.register_blueprint(busca_bp) 
app.register_blueprint(listas_bp, url_prefix='/listas')
app.register_blueprint(detalhes_bp, url_prefix='/detalhes')
app.register_blueprint(arquivos_bp)
app.register_blueprint(perfil_bp)

# Inicia o agendador de ranking (atualização diária do CSV)
agendador.iniciar()

if __name__ == '__main__':
    try:
        # Remova debug=True para produção
        app.run()
    finally:
        # Para o agendador ao encerrar a aplicação
        agendador.parar()
