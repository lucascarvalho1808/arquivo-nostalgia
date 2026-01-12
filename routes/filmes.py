from flask import Blueprint, render_template, request, jsonify
from services.api_tmdb import buscar_catalogo_filmes, buscar_filmes_por_genero

filmes_bp = Blueprint('filmes', __name__)

@filmes_bp.route('/filmes')
def index():
    lista_filmes = buscar_catalogo_filmes(pagina=1)
    return render_template('conteudo/filmes.html', filmes=lista_filmes)

@filmes_bp.route('/api/filmes')
def api_filmes():
    '''API que retorna filmes populares em JSON para o botão 'Ver mais'.'''
    pagina = request.args.get('pagina', 1, type=int)
    lista_filmes = buscar_catalogo_filmes(pagina=pagina)
    return jsonify(lista_filmes)

@filmes_bp.route('/api/filmes/filtrar')
def api_filmes_filtrar():
    '''API que retorna filmes filtrados por gênero.'''
    generos = request.args.get('generos', '')  
    pagina = request.args.get('pagina', 1, type=int)
    
    if generos:
        lista_filmes = buscar_filmes_por_genero(generos=generos, pagina=pagina)
    else:
        lista_filmes = buscar_catalogo_filmes(pagina=pagina)
    
    return jsonify(lista_filmes)