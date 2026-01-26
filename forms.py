from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class CadastroForm(FlaskForm):
    """
    Formulário de cadastro de novo usuário.
    Campos: nome, e-mail, senha, confirmação de senha.
    """
    
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=20)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem ser iguais.')])
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):
    """
    Formulário de login do usuário.
    Campos: e-mail e senha.
    """
    
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class EsqueceuSenhaForm(FlaskForm):
    """
    Formulário para solicitação de recuperação de senha.
    Campo: e-mail.
    """
    
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar Link de Recuperação')

class RedefinirSenhaForm(FlaskForm):
    """
    Formulário para redefinição de senha.
    Campos: nova senha e confirmação de nova senha.
    """
    
    senha = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6, max=20)])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem ser iguais.')])
    submit = SubmitField('Alterar Senha')