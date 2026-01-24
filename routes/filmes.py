from flask import Blueprint, render_template, request, jsonify
from services.api_tmdb import buscar_catalogo_filmes, buscar_filmes_por_genero

# Cria o Blueprint para rotas relacionadas a filmes
filmes_bp = Blueprint('filmes', __name__)

@filmes_bp.route('/filmes')
def index():
    """
    Página principal de filmes.
    Exibe uma lista de filmes populares (primeira página).
    """
    lista_filmes = buscar_catalogo_filmes(pagina=1)
    return render_template('conteudo/filmes.html', filmes=lista_filmes)

@filmes_bp.route('/api/filmes')
def api_filmes():
    """
    API que retorna filmes populares em formato JSON.
    Usada para o botão 'Ver mais' na página de filmes.
    """
    pagina = request.args.get('pagina', 1, type=int)
    lista_filmes = buscar_catalogo_filmes(pagina=pagina)
    return jsonify(lista_filmes)

@filmes_bp.route('/api/filmes/filtrar')
def api_filmes_filtrar():
    """
    API que retorna filmes filtrados por gênero em formato JSON.
    """
    generos = request.args.get('generos', '')  
    pagina = request.args.get('pagina', 1, type=int)
    
    if generos:
        # Busca filmes filtrados por gênero
        lista_filmes = buscar_filmes_por_genero(generos=generos, pagina=pagina)
    else:
        # Se não houver filtro, retorna filmes populares
        lista_filmes = buscar_catalogo_filmes(pagina=pagina)
    
    return jsonify(lista_filmes)