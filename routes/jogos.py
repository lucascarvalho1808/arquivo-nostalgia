from flask import Blueprint, render_template, request, jsonify
from services.api_rawg import buscar_catalogo_jogos, buscar_jogos_por_genero

jogos_bp = Blueprint('jogos', __name__)

@jogos_bp.route('/jogos')
def index():
    lista_jogos = buscar_catalogo_jogos(pagina=1)
    return render_template('conteudo/jogos.html', jogos=lista_jogos)

@jogos_bp.route('/api/jogos')
def api_jogos():
    '''API que retorna jogos populares em JSON para o botão 'Ver mais'.'''
    pagina = request.args.get('pagina', 1, type=int)
    lista_jogos = buscar_catalogo_jogos(pagina=pagina)
    return jsonify(lista_jogos)

@jogos_bp.route('/api/jogos/filtrar')
def api_jogos_filtrar():
    '''API que retorna jogos filtrados por gênero.'''
    generos = request.args.get('generos', '')
    pagina = request.args.get('pagina', 1, type=int)
    
    if generos:
        lista_jogos = buscar_jogos_por_genero(generos=generos, pagina=pagina)
    else:
        lista_jogos = buscar_catalogo_jogos(pagina=pagina)
    
    return jsonify(lista_jogos)