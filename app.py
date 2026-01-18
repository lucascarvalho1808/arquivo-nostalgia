from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from routes.extensions import supabase  

# Importando os Blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.filmes import filmes_bp
from routes.series import series_bp
from routes.jogos import jogos_bp
from routes.busca import busca_bp  
from routes.listas import listas_bp
from routes.detalhes import detalhes_bp

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

# Configuração do LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
# IMPORTANTE: Note que agora referenciamos 'auth.login' em vez de apenas 'login'
login_manager.login_view = 'auth.login' 
login_manager.login_message = "Faça login para continuar." 
login_manager.login_message_category = "info" 

@login_manager.user_loader
def load_user(user_id):
    try:
        user_response = supabase.auth.get_user()
        if user_response and user_response.user and user_response.user.id == user_id:
            user_data = user_response.user
            username = user_data.user_metadata.get('username', 'Usuário')
            return User(id=user_data.id, email=user_data.email, username=username)
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

# lembrar de tirar parte do debug ao final do projeto 
if __name__ == '__main__':
    app.run(debug=True)
# fim do debug