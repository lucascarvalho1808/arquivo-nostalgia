from flask import Blueprint, render_template, request, jsonify
from services.api_tmdb import buscar_filmes, buscar_series
from services.api_rawg import buscar_jogos

# Blueprint para rotas de busca (filmes, séries e jogos)
busca_bp = Blueprint('busca', __name__)

# Busca geral (página inicial) - retorna página de resultados
@busca_bp.route('/busca')
def busca_geral():
    """
    Rota para busca geral no site.
    Pesquisa filmes, séries e jogos usando o termo informado pelo usuário.
    Exibe resultados ou página de 'sem resultados' se nada for encontrado.
    """
    termo = request.args.get('q', '').strip()
    
    if not termo:
        # Se nenhum termo foi informado, exibe página de sem resultados
        return render_template('busca/sem_resultados.html', termo=termo)
    
    # Busca em todas as APIs (limite de 200 resultados por tipo)
    filmes = buscar_filmes(termo, max_resultados=200)
    series = buscar_series(termo, max_resultados=200)
    jogos = buscar_jogos(termo, max_resultados=200)
    
    # Soma total de resultados encontrados
    total_resultados = len(filmes) + len(series) + len(jogos)
    
    if total_resultados == 0:
        # Se nada foi encontrado, exibe página de sem resultados
        return render_template('busca/sem_resultados.html', termo=termo)
    
    # Exibe página de resultados com todos os dados encontrados
    return render_template(
        'busca/resultados.html',
        termo=termo,
        filmes=filmes,
        series=series,
        jogos=jogos,
        total=total_resultados
    )

# API de busca de filmes (para a página de filmes)
@busca_bp.route('/api/busca/filmes')
def api_busca_filmes():
    """
    API para buscar filmes pelo termo informado.
    Retorna lista de filmes em formato JSON.
    """
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return jsonify([])
    
    filmes = buscar_filmes(termo, max_resultados=200)
    return jsonify(filmes)

# API de busca de séries (para a página de séries)
@busca_bp.route('/api/busca/series')
def api_busca_series():
    """
    API para buscar séries pelo termo informado.
    Retorna lista de séries em formato JSON.
    """
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return jsonify([])
    
    series = buscar_series(termo, max_resultados=200)
    return jsonify(series)

# API de busca de jogos (para a página de jogos)
@busca_bp.route('/api/busca/jogos')
def api_busca_jogos():
    """
    API para buscar jogos pelo termo informado.
    Retorna lista de jogos em formato JSON.
    """
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return jsonify([])
    
    jogos = buscar_jogos(termo, max_resultados=200)
    return jsonify(jogos)