from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from forms import CadastroForm, LoginForm, EsqueceuSenhaForm, RedefinirSenhaForm
from models import User
from routes.extensions import supabase  

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login')) 
        except Exception as e:
            error_message = str(e)
            if 'User already registered' in error_message:
                flash('Este e-mail já está cadastrado.', 'danger')
            else:
                flash(f'Erro no registro: {error_message}', 'danger')
    # Formulário para o template para ser renderizado            
    return render_template('auth/cadastro.html', form=form)

# Rota de login
@auth_bp.route('/login', methods=['GET', 'POST'])
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
            return redirect(next_page or url_for('main.index'))
            
        except Exception as e:
            error_message = str(e)
            if 'Invalid login credentials' in error_message:
                flash('E-mail ou senha inválidos.', 'danger')
            else:
                flash(f'Erro ao fazer login: {error_message}', 'danger')
                
    return render_template('auth/login.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    # 1. Desloga do Supabase
    supabase.auth.sign_out()
    
    # 2. Limpa a sessão do Flask
    logout_user()
    flash('Você saiu com sucesso.', 'info')
    
    #  Redireciona para a página inicial (index) 
    return redirect(url_for('main.index')) 

@auth_bp.route('/esqueceu-senha', methods=['GET', 'POST'])
def forgot_password():
    form = EsqueceuSenhaForm()
    if form.validate_on_submit():
        try:
            # Supabase envia um e-mail com um link para redefinir a senha
            supabase.auth.reset_password_email(form.email.data, options={
                "redirect_to": url_for('auth.reset_password', _external=True) 
            })
            flash('Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.', 'info')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Erro ao enviar e-mail: {str(e)}', 'danger')
            
    return render_template('auth/esqueceu_senha.html', form=form)

@auth_bp.route('/redefinir-senha', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Erro ao atualizar senha: {str(e)}', 'danger')
            
    return render_template('auth/redefinir_senha.html', form=form)