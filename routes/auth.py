from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from routes.extensions import supabase
from forms import LoginForm, CadastroForm, EsqueceuSenhaForm, RedefinirSenhaForm 

auth_bp = Blueprint('auth', __name__)

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
            
            # 2. Se chegou aqui, o login funcionou
            user_data = res.user
            username = user_data.user_metadata.get('username', 'Usuário')
            user = User(id=user_data.id, email=user_data.email, username=username)
            
            # 3. Loga o usuário no Flask
            login_user(user)
            
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index')) 
            
        except Exception as e:
            error_message = str(e)
            if 'Invalid login credentials' in error_message:
                flash('E-mail ou senha inválidos.', 'danger')
            else:
                flash(f'Erro ao fazer login. Tente novamente.', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
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
            flash(f'Erro no registro: {str(e)}', 'danger')
    
    return render_template('auth/cadastro.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    try:
        supabase.auth.sign_out()
        session.clear()
    except Exception as e:
        print(f"Erro no logout: {e}")
    
    logout_user()
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/esqueceu-senha', methods=['GET', 'POST'])
def esqueceu_senha():
    form = EsqueceuSenhaForm()
    
    if form.validate_on_submit():
        try:
            # URL completa de redirecionamento
            url_redirecionamento = url_for('auth.redefinir_senha', _external=True)
            
            supabase.auth.reset_password_email(
                form.email.data,
                options={
                    "redirect_to": url_redirecionamento
                }
            )
            
            flash('Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha. Verifique sua caixa de entrada.', 'info')
            return redirect(url_for('auth.login'))
        except Exception as e:
            # Não revela se o e-mail existe ou não 
            flash('Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.', 'info')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/esqueceu_senha.html', form=form)


@auth_bp.route('/redefinir-senha', methods=['GET', 'POST'])
def redefinir_senha():
    """
    Esta rota é acessada quando o usuário clica no link do e-mail.
    O Supabase envia tokens via fragment (#) na URL.
    """
    form = RedefinirSenhaForm()
    
    if form.validate_on_submit():
        try:
            # Captura o token de acesso enviado via JavaScript do template
            access_token = request.form.get('access_token')
            
            if not access_token:
                flash('Token de autenticação não encontrado. Solicite um novo link.', 'danger')
                return redirect(url_for('auth.esqueceu_senha'))
            
            # Define a sessão do usuário usando o token
            supabase.auth.set_session(access_token, request.form.get('refresh_token', ''))
            
            # Atualiza a senha
            supabase.auth.update_user({
                "password": form.senha.data
            })
            
            # Faz logout para segurança
            supabase.auth.sign_out()
            
            flash('Sua senha foi alterada com sucesso! Faça login com a nova senha.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash(f'Erro ao atualizar senha: {str(e)}', 'danger')
            
    return render_template('auth/redefinir_senha.html', form=form)