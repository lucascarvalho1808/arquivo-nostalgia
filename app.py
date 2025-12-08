from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, url_for
import os
from supabase import create_client, Client
from forms import CadastroForm, LoginForm 

load_dotenv()

app = Flask(__name__)
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

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

# Rota de login (provisoria)
@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Página de login (em construção)"

# lembrar de tirar parte do debug ao final do projeto 
if __name__ == '__main__':
    app.run(debug=True)
# fim do debug