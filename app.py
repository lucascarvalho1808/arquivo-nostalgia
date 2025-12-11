from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, url_for
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from supabase import create_client, Client
from forms import CadastroForm, LoginForm, EsqueceuSenhaForm, RedefinirSenhaForm 
from models import User
from services.api_rawg import buscar_jogos_populares    
from services.curiosidade_do_dia import get_curiosidade_diaria
from services.api_tmdb import (
    buscar_filmes_populares, 
    buscar_series_populares, 
    buscar_filmes_classicos,  
    buscar_series_nostalgia   
)
import random

load_dotenv()

app = Flask(__name__)
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Faça login para continuar." 
login_manager.login_message_category = "info" 

@login_manager.user_loader
def load_user(user_id):
    try:
        # Usa a sessão do Supabase para obter o usuário autenticado
        user_response = supabase.auth.get_user()
        
        # Verifica se a chamada foi bem-sucedida e se o ID corresponde
        if user_response and user_response.user and user_response.user.id == user_id:
            user_data = user_response.user
            # Extrai o username dos metadados
            username = user_data.user_metadata.get('username', 'Usuário')
            
            # Cria e retorna o objeto User para o flask-login
            return User(id=user_data.id, email=user_data.email, username=username)
            
    except Exception as e:
        # Em caso de qualquer erro, não carrega o usuário
        print(f"Erro ao carregar usuário da sessão: {e}")
        
    return None

@app.route('/')
def index():
    # Buscando dados das APIs
    filmes_populares = buscar_filmes_populares()
    series_populares = buscar_series_populares()
    jogos_populares = buscar_jogos_populares() 
    
    # Buscando as novas categorias
    filmes_classicos = buscar_filmes_classicos()
    series_nostalgia = buscar_series_nostalgia()

    # Lógica original restaurada (Cache + Curiosidade do Dia)
    curiosidade = get_curiosidade_diaria()

    return render_template(
        'index.html',
        filmes=filmes_populares,
        series=series_populares,
        jogos=jogos_populares,
        curiosidade=curiosidade,
        filmes_destaque=filmes_classicos,
        series_nostalgia=series_nostalgia
    )

@app.route('/cadastro', methods=['GET', 'POST'])
def register():
    form = CadastroForm() # Cria uma instância do formulário
    if form.validate_on_submit(): # Valida no POST e se os dados são válidos
        try:
            user = supabase.auth.sign_up({
                "email": form.email.data, 
                "password": form.senha.data,
                "options": {
                    "data": {
                        "username": form.nome.data 
                    }
                }
            })
            flash('Registro realizado com sucesso. Verifique seu e-mail para confirmar a conta.', 'success')
            return redirect(url_for('login')) 
        except Exception as e:
            error_message = str(e)
            if 'User already registered' in error_message:
                flash('Este e-mail já está cadastrado.', 'danger')
            else:
                flash(f'Erro no registro: {error_message}', 'danger')
    # Passe o formulário para o template para ser renderizado
    return render_template('auth/cadastro.html', form=form)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # 1. Tenta autenticar no Supabase
            res = supabase.auth.sign_in_with_password({
                "email": form.email.data,
                "password": form.senha.data
            })
            
            # 2. Se chegou aqui, o login no Supabase funcionou.
            user_data = res.user
            username = user_data.user_metadata.get('username', 'Usuário')
            user = User(id=user_data.id, email=user_data.email, username=username)
            
            # 3. Loga o usuário na sessão do Flask
            login_user(user)
            
            flash('Login realizado com sucesso!', 'success')
            
            # Redireciona para a página que o usuário tentou acessar ou para a home
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
            
        except Exception as e:
            error_message = str(e)
            if 'Invalid login credentials' in error_message:
                flash('E-mail ou senha inválidos.', 'danger')
            else:
                flash(f'Erro ao fazer login: {error_message}', 'danger')
                
    return render_template('auth/login.html', form=form)

@app.route("/logout")
@login_required # Garante que apenas quem está logado pode acessar essa rota
def logout():
    # 1. Desloga do Supabase (invalida o token)
    supabase.auth.sign_out()
    
    # 2. Limpa a sessão do Flask
    logout_user()
    
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('login')) 

@app.route('/esqueceu-senha', methods=['GET', 'POST'])
def forgot_password():
    form = EsqueceuSenhaForm()
    if form.validate_on_submit():
        try:
            # Supabase envia um e-mail com um link para redefinir a senha
            supabase.auth.reset_password_email(form.email.data, options={
                "redirect_to": url_for('reset_password', _external=True) 
            })
            flash('Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.', 'info')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Erro ao enviar e-mail: {str(e)}', 'danger')
            
    return render_template('auth/esqueceu_senha.html', form=form)

@app.route('/redefinir-senha', methods=['GET', 'POST'])
def reset_password():
    # Esta rota é acessada quando o usuário clicar no link do e-mail.    
    form = RedefinirSenhaForm()
    if form.validate_on_submit():
        try:
            # Atualiza a senha do usuário logado
            supabase.auth.update_user({
                "password": form.senha.data
            })
            flash('Sua senha foi alterada com sucesso! Faça login novamente.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Erro ao atualizar senha: {str(e)}', 'danger')
            
    return render_template('auth/redefinir_senha.html', form=form)

#Rotas Protegidas (provisórias)

@app.route('/perfil')
@login_required
def perfil():
    # Exibe o nome do usuário logado para provar que o login funcionou
    return f"<h1>Página de Perfil</h1><p>Bem-vindo, {current_user.username}!</p>"

@app.route('/criar-arquivo-nostalgia')
@login_required
def criar_arquivo():
    return "<h1>Criar Arquivo Nostalgia</h1><p>Aqui ficará o formulário de criação.</p>"

@app.route('/meus-arquivos')
@login_required
def meus_arquivos():
    return "<h1>Meus Arquivos</h1><p>Lista dos arquivos que você criou.</p>"

# lembrar de tirar parte do debug ao final do projeto 
if __name__ == '__main__':
    app.run(debug=True)
# fim do debug