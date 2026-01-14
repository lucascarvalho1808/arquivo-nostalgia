from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from models import User
from routes.extensions import supabase
from forms import LoginForm, CadastroForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Criar o formulário
    
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data
        
        try:
            # Tenta fazer login com Supabase
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": senha
            })
            
            if auth_response and auth_response.user:
                user_data = auth_response.user
                username = user_data.user_metadata.get('username', 'Usuário')
                user = User(id=user_data.id, email=user_data.email, username=username)
                login_user(user)
                
                # Salvar o access_token na sessão para RLS
                session['access_token'] = auth_response.session.access_token
                session['refresh_token'] = auth_response.session.refresh_token
                
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Email ou senha incorretos.', 'danger')
        except Exception as e:
            print(f"Erro no login: {e}")
            flash('Erro ao fazer login. Tente novamente.', 'danger')
    
    return render_template('auth/login.html', form=form)  # Passar o form aqui


@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()  # Criar o formulário
    
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data
        username = form.username.data
        
        try:
            # Registra no Supabase
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": senha,
                "options": {
                    "data": {
                        "username": username
                    }
                }
            })
            
            if auth_response.user:
                flash('Cadastro realizado! Verifique seu email para confirmar.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Erro ao cadastrar. Tente novamente.', 'danger')
        except Exception as e:
            print(f"Erro no cadastro: {e}")
            flash('Erro ao cadastrar. Email já pode estar em uso.', 'danger')
    
    return render_template('auth/cadastro.html', form=form)  # Passar o form aqui


@auth_bp.route('/logout')
@login_required
def logout():
    try:
        supabase.auth.sign_out()
        session.clear()  # Limpa a sessão incluindo os tokens
    except Exception as e:
        print(f"Erro no logout: {e}")
    
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/esqueceu-senha', methods=['GET', 'POST'])
def esqueceu_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        
        try:
            supabase.auth.reset_password_email(email)
            flash('Email de recuperação enviado! Verifique sua caixa de entrada.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"Erro ao enviar email de recuperação: {e}")
            flash('Erro ao enviar email de recuperação.', 'danger')
    
    return render_template('auth/esqueceu_senha.html')


@auth_bp.route('/redefinir-senha', methods=['GET', 'POST'])
def redefinir_senha():
    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')
        
        try:
            supabase.auth.update_user({"password": nova_senha})
            flash('Senha redefinida com sucesso!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"Erro ao redefinir senha: {e}")
            flash('Erro ao redefinir senha.', 'danger')
    
    return render_template('auth/redefinir_senha.html')