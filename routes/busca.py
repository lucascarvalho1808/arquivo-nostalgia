from flask import Blueprint, render_template, request, jsonify
from services.api_tmdb import buscar_filmes, buscar_series
from services.api_rawg import buscar_jogos

busca_bp = Blueprint('busca', __name__)

# Busca geral (página inicial) - retorna página de resultados
@busca_bp.route('/busca')
def busca_geral():
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return render_template('busca/sem_resultados.html', termo=termo)
    
    # Busca em todas as APIs (com até 200 resultados cada = 600 total)
    filmes = buscar_filmes(termo, max_resultados=200)
    series = buscar_series(termo, max_resultados=200)
    jogos = buscar_jogos(termo, max_resultados=200)
    
    # Verifica se encontrou algo
    total_resultados = len(filmes) + len(series) + len(jogos)
    
    if total_resultados == 0:
        return render_template('busca/sem_resultados.html', termo=termo)
    
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
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return jsonify([])
    
    filmes = buscar_filmes(termo, max_resultados=200)
    return jsonify(filmes)

# API de busca de séries (para a página de séries)
@busca_bp.route('/api/busca/series')
def api_busca_series():
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return jsonify([])
    
    series = buscar_series(termo, max_resultados=200)
    return jsonify(series)

# API de busca de jogos (para a página de jogos)
@busca_bp.route('/api/busca/jogos')
def api_busca_jogos():
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return jsonify([])
    
    jogos = buscar_jogos(termo, max_resultados=200)
    return jsonify(jogos)