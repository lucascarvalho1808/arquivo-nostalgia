from flask import Blueprint, render_template, request, jsonify
from services.api_tmdb import buscar_catalogo_series, buscar_series_por_genero

# Cria o Blueprint para rotas relacionadas a séries
series_bp = Blueprint('series', __name__)

@series_bp.route('/series')
def index():
    """
    Página principal de séries.
    Exibe uma lista de séries populares (primeira página).
    """
    lista_series = buscar_catalogo_series(pagina=1)
    return render_template('conteudo/series.html', series=lista_series)

@series_bp.route('/api/series')
def api_series():
    """
    API que retorna séries populares em formato JSON.
    Usada para o botão 'Ver mais' na página de séries.
    """
    pagina = request.args.get('pagina', 1, type=int)
    lista_series = buscar_catalogo_series(pagina=pagina)
    return jsonify(lista_series)

@series_bp.route('/api/series/filtrar')
def api_series_filtrar():
    """
    API que retorna séries filtradas por gênero em formato JSON.
    """
    generos = request.args.get('generos', '')
    pagina = request.args.get('pagina', 1, type=int)
    
    if generos:
        # Busca séries filtradas por gênero
        lista_series = buscar_series_por_genero(generos=generos, pagina=pagina)
    else:
        # Se não houver filtro, retorna séries populares
        lista_series = buscar_catalogo_series(pagina=pagina)
    
    return jsonify(lista_series)