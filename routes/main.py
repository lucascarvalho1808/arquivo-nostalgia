from flask import Blueprint, render_template, session  
from flask_login import login_required, current_user
from services.api_rawg import buscar_jogos_populares
from services.curiosidade_do_dia import get_curiosidade_diaria
from services.api_tmdb import (
    buscar_filmes_populares, 
    buscar_series_populares, 
    buscar_filmes_classicos,  
    buscar_series_nostalgia
)

# Cria o Blueprint principal para rotas públicas e institucionais
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Página inicial do site.
    Busca dados populares das APIs e exibe curiosidade do dia.
    Incrementa o contador de acessos à página inicial na sessão.
    """
    # Incrementa o contador de acessos à página inicial na sessão
    session['acessos_index'] = session.get('acessos_index', 0) + 1

    # Buscando dados das APIs externas
    filmes_populares = buscar_filmes_populares()
    series_populares = buscar_series_populares()
    jogos_populares = buscar_jogos_populares() 
    
    # Buscando outras categorias
    filmes_classicos = buscar_filmes_classicos()
    series_nostalgia = buscar_series_nostalgia()
    
    # Busca a curiosidade do dia 
    curiosidade = get_curiosidade_diaria()

    # Renderiza o template da página inicial com todos os dados
    return render_template(
        'index.html',
        filmes=filmes_populares,
        series=series_populares,
        jogos=jogos_populares,
        curiosidade=curiosidade,
        filmes_destaque=filmes_classicos,
        series_nostalgia=series_nostalgia
    )

@main_bp.route('/termos')
def termos():
    """
    Página de Termos de Uso do site.
    """
    return render_template('termos.html')

@main_bp.route('/privacidade')
def privacidade():
    """
    Página de Política de Privacidade do site.
    """
    return render_template('privacidade.html')