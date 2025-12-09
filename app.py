from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, url_for
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from supabase import create_client, Client
from forms import CadastroForm, LoginForm 
from models import User

load_dotenv()

app = Flask(__name__)
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
    return render_template('index.html')

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

# lembrar de tirar parte do debug ao final do projeto 
if __name__ == '__main__':
    app.run(debug=True)
# fim do debug