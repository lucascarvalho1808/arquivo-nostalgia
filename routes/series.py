from flask import Blueprint, render_template, request, jsonify
from services.api_tmdb import buscar_catalogo_series, buscar_series_por_genero

series_bp = Blueprint('series', __name__)

@series_bp.route('/series')
def index():
    lista_series = buscar_catalogo_series(pagina=1)
    return render_template('conteudo/series.html', series=lista_series)

@series_bp.route('/api/series')
def api_series():
    '''API que retorna séries populares em JSON para o botão 'Ver mais'.'''
    pagina = request.args.get('pagina', 1, type=int)
    lista_series = buscar_catalogo_series(pagina=pagina)
    return jsonify(lista_series)

@series_bp.route('/api/series/filtrar')
def api_series_filtrar():
    '''API que retorna séries filtradas por gênero.'''
    generos = request.args.get('generos', '')
    pagina = request.args.get('pagina', 1, type=int)
    
    if generos:
        lista_series = buscar_series_por_genero(generos=generos, pagina=pagina)
    else:
        lista_series = buscar_catalogo_series(pagina=pagina)
    
    return jsonify(lista_series)