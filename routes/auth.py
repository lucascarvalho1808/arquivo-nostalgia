from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from routes.extensions import supabase
from forms import LoginForm, CadastroForm, EsqueceuSenhaForm, RedefinirSenhaForm 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota de login do usuário.
    Autentica no Supabase, faz login no Flask e armazena tokens na sessão.
    """
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # 1. Tenta autenticar no Supabase
            res = supabase.auth.sign_in_with_password({
                "email": form.email.data,
                "password": form.senha.data
            })
            
            # 2. Extrai user e session/token (tratamento defensivo)
            user_data = None
            access_token = None
            refresh_token = None

            # Extrai dados do usuário do resultado da autenticação
            if hasattr(res, "user"):
                user_data = res.user
            elif isinstance(res, dict):
                user_data = res.get("user")

            # Extrai tokens de sessão do resultado
            if hasattr(res, "session") and res.session:
                session_obj = res.session
                access_token = getattr(session_obj, "access_token", None) or (session_obj.get("access_token") if isinstance(session_obj, dict) else None)
                refresh_token = getattr(session_obj, "refresh_token", None) or (session_obj.get("refresh_token") if isinstance(session_obj, dict) else None)
            elif isinstance(res, dict) and res.get("session"):
                access_token = res["session"].get("access_token")
                refresh_token = res["session"].get("refresh_token")
            else:
                # Fallback: se houver chaves planas
                access_token = res.get("access_token") if isinstance(res, dict) else getattr(res, "access_token", None)
                refresh_token = res.get("refresh_token") if isinstance(res, dict) else getattr(res, "refresh_token", None)

            # 3. Cria User e faz login no Flask se autenticação OK
            if user_data:
                username = user_data.user_metadata.get('username', 'Usuário') if hasattr(user_data, "user_metadata") else user_data.get("user_metadata", {}).get("username", "Usuário")
                user = User(
                    id=user_data.id if hasattr(user_data, "id") else user_data.get("id"),
                    email=user_data.email if hasattr(user_data, "email") else user_data.get("email"),
                    username=username,
                    created_at=getattr(user_data, "created_at", None) if hasattr(user_data, "created_at") else user_data.get("created_at")
                )
                login_user(user)

                # 4. Salva tokens na sessão para uso em chamadas server-side (supabase REST)
                if access_token:
                    session['supabase_access_token'] = access_token
                if refresh_token:
                    session['supabase_refresh_token'] = refresh_token

                flash('Login realizado com sucesso!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.index')) 
            else:
                flash('Erro ao fazer login. Tente novamente.', 'danger')
            
        except Exception as e:
            error_message = str(e)
            if 'Invalid login credentials' in error_message:
                flash('E-mail ou senha inválidos.', 'danger')
            else:
                flash(f'Erro ao fazer login. Tente novamente.', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    Rota de cadastro de novo usuário.
    Registra o usuário no Supabase e envia confirmação por e-mail.
    """
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
    """
    Rota de logout do usuário.
    Encerra a sessão no Supabase, limpa a sessão Flask e faz logout.
    """
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
    """
    Rota para solicitação de redefinição de senha.
    Envia e-mail com link de redefinição usando Supabase.
    """
    form = EsqueceuSenhaForm()
    
    if form.validate_on_submit():
        try:
            # URL completa de redirecionamento após redefinição
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
    Rota acessada pelo link enviado por e-mail para redefinir senha.
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
            
            # Define a sessão do usuário usando o token recebido
            supabase.auth.set_session(access_token, request.form.get('refresh_token', ''))
            
            # Atualiza a senha do usuário
            supabase.auth.update_user({
                "password": form.senha.data
            })
            
            # Faz logout para segurança após alteração de senha
            supabase.auth.sign_out()
            
            flash('Sua senha foi alterada com sucesso! Faça login com a nova senha.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash(f'Erro ao atualizar senha: {str(e)}', 'danger')
            
    return render_template('auth/redefinir_senha.html', form=form)