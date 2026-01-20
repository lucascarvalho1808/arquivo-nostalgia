from flask import Blueprint, render_template
from flask_login import login_required, current_user
from services.api_rawg import buscar_jogos_populares
from services.curiosidade_do_dia import get_curiosidade_diaria
from services.api_tmdb import (
    buscar_filmes_populares, 
    buscar_series_populares, 
    buscar_filmes_classicos,  
    buscar_series_nostalgia
)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Buscando dados das APIs
    filmes_populares = buscar_filmes_populares()
    series_populares = buscar_series_populares()
    jogos_populares = buscar_jogos_populares() 
    
    # Buscando outras categorias
    filmes_classicos = buscar_filmes_classicos()
    series_nostalgia = buscar_series_nostalgia()
    
    # Lógica (Cache + Curiosidade do Dia)
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

@main_bp.route('/perfil')
@login_required
def perfil():
    return f"<h1>Página de Perfil</h1><p>Bem-vindo, {current_user.username}!</p>"

@main_bp.route('/criar-arquivo-nostalgia')
@login_required
def criar_arquivo():
    return "<h1>Criar Arquivo Nostalgia</h1><p>Aqui ficará o formulário de criação.</p>"

@main_bp.route('/termos')
def termos():
    return render_template('termos.html')

@main_bp.route('/privacidade')
def privacidade():
    return render_template('privacidade.html')