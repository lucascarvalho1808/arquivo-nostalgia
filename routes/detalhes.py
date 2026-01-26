from flask import Blueprint, render_template, abort
from services.api_tmdb import buscar_detalhes_filme, buscar_detalhes_serie
from services.api_rawg import buscar_detalhes_jogo
from services.api_steam import obter_trailer_steam  
from datetime import datetime

# Blueprint para rotas de detalhes de filmes, séries e jogos
detalhes_bp = Blueprint('detalhes', __name__)

@detalhes_bp.app_template_filter('formato_data')
def formato_data(data_str):
    """
    Filtro de template para converter data.
    """
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        return data.strftime('%d/%m/%Y')
    except:
        return data_str

@detalhes_bp.app_template_filter('formato_duracao')
def formato_duracao(minutos):
    """
    Filtro de template para converter minutos em formato 'Xh Ym'.
    """
    horas = minutos // 60
    mins = minutos % 60
    return f"{horas}h {mins:02d}m"

@detalhes_bp.route('/filme/<int:filme_id>')
def filme(filme_id):
    """
    Exibe detalhes de um filme.
    Busca dados na API TMDB, processa informações e renderiza o template.
    """
    try:
        # Busca detalhes do filme na API TMDB
        conteudo = buscar_detalhes_filme(filme_id)
        
        if not conteudo:
            abort(404)
        
        # Processa classificação indicativapara o Brasil
        classificacao = 'N/A'
        release_dates = conteudo.get('release_dates', {}).get('results', [])
        br_release = next((item for item in release_dates if item['iso_3166_1'] == 'BR'), None)
        if br_release:
            for release in br_release['release_dates']:
                if release.get('certification'):
                    classificacao = release['certification']
                    break

        # Processa gêneros em string separada por vírgula
        generos = ', '.join([g['name'] for g in conteudo.get('genres', [])])
        
        # Busca elenco e equipe técnica
        credits = conteudo.get('credits', {})
        elenco = credits.get('cast', [])[:12]
        equipe = [p for p in credits.get('crew', []) 
                  if p['job'] in ['Director', 'Screenplay', 'Original Music Composer']]
        
        # Busca trailer do YouTube
        videos = conteudo.get('videos', {}).get('results', [])
        trailer = next((v for v in videos if v['type'] == 'Trailer' and v['site'] == 'YouTube'), None)
        trailer_url = f"https://www.youtube.com/watch?v={trailer['key']}" if trailer else None
        
        return render_template('detalhes_fimes_series.html',
                             conteudo=conteudo,
                             generos=generos,
                             elenco=elenco,
                             equipe=equipe,
                             classificacao=classificacao, 
                             trailer_url=trailer_url)
    
    except Exception as e:
        print(f"Erro ao buscar detalhes do filme: {e}")
        abort(500)

@detalhes_bp.route('/serie/<int:serie_id>')
def serie(serie_id):
    """
    Exibe detalhes de uma série.
    Busca dados na API TMDB, adapta campos e renderiza o template.
    """
    try:
        conteudo = buscar_detalhes_serie(serie_id)
        
        if not conteudo:
            abort(404)
        
        # Adapta campos para compatibilidade com template de filme
        conteudo['title'] = conteudo.get('name', 'Título não disponível')
        conteudo['release_date'] = conteudo.get('first_air_date')
        
        # Processa classificação indicativa para o Brasil
        classificacao = 'N/A'
        content_ratings = conteudo.get('content_ratings', {}).get('results', [])
        br_rating = next((item for item in content_ratings if item['iso_3166_1'] == 'BR'), None)
        if br_rating:
            classificacao = br_rating.get('rating', 'N/A')

        # Processa gêneros em string separada por vírgula
        generos = ', '.join([g['name'] for g in conteudo.get('genres', [])])
        
        # Busca elenco
        credits = conteudo.get('credits', {})
        elenco = credits.get('cast', [])[:12]
        
        # Monta equipe técnica 
        equipe = []
        crew = credits.get('crew', [])
        # Adiciona criadores
        created_by = conteudo.get('created_by', [])
        for creator in created_by:
            equipe.append({
                'name': creator['name'],
                'job': 'Criador(a)'
            })
        # Adiciona produtores executivos
        episodic_producers = [p for p in crew if p['job'] == 'Executive Producer']
        for prod in episodic_producers:
            if len(equipe) >= 3: break
            if not any(e['name'] == prod['name'] for e in equipe):
                equipe.append({'name': prod['name'], 'job': 'Prod. Executivo'})
        # Adiciona músicos, se houver espaço
        if len(equipe) < 3:
            musicians = [p for p in crew if 'Music' in p['job'] or p['job'] == 'Original Music Composer']
            for musico in musicians:
                if len(equipe) >= 3: break
                if not any(e['name'] == musico['name'] for e in equipe):
                    equipe.append({'name': musico['name'], 'job': 'Música'})
        equipe = equipe[:3]
        
        # Busca trailer do YouTube
        videos = conteudo.get('videos', {}).get('results', [])
        trailer = next((v for v in videos if v['type'] == 'Trailer' and v['site'] == 'YouTube'), None)
        if not trailer:
             trailer = next((v for v in videos if v['site'] == 'YouTube' and 'Trailer' in v['type']), None)
        trailer_url = f"https://www.youtube.com/watch?v={trailer['key']}" if trailer else None
        
        return render_template('detalhes_fimes_series.html',
                             conteudo=conteudo,
                             generos=generos,
                             elenco=elenco,
                             equipe=equipe,
                             classificacao=classificacao,
                             trailer_url=trailer_url)
    
    except Exception as e:
        print(f"Erro ao buscar detalhes da série: {e}")
        abort(500)

# Dicionário de tradução de classificações para ClassInd (Brasil)
CLASSIFICACAO_TRADUCAO = {
    'Everyone': 'L',           # Livre
    'Everyone 10+': '10',      # 10 anos
    'Teen': '12',              # 12 anos
    'Mature 17+': '18',        # 18 anos
    'Mature': '18',            # 18 anos (variação sem número)
    'Adults Only 18+': '18',   # 18 anos
    'Adults Only': '18',       # 18 anos (variação sem número)
    'Rating Pending': 'N/A'    # Classificação pendente
}

# Dicionário de tradução de gêneros de jogos
GENEROS_TRADUCAO = {
    'Action': 'Ação',
    'Adventure': 'Aventura',
    'RPG': 'RPG',
    'Shooter': 'Tiro',
    'Puzzle': 'Quebra-cabeça',
    'Racing': 'Corrida',
    'Sports': 'Esportes',
    'Strategy': 'Estratégia',
    'Fighting': 'Luta',
    'Platformer': 'Plataforma',
    'Simulation': 'Simulação',
    'Casual': 'Casual',
    'Indie': 'Indie',
    'Massively Multiplayer': 'MMO',
    'Family': 'Família',
    'Board Games': 'Jogos de Tabuleiro',
    'Educational': 'Educacional',
    'Card': 'Cartas'
}

@detalhes_bp.route('/jogo/<int:jogo_id>')
def jogo(jogo_id):
    """
    Exibe detalhes de um jogo.
    Busca dados na API RAWG, traduz campos e busca trailer.
    """
    try:
        jogo = buscar_detalhes_jogo(jogo_id)
        
        if not jogo:
            abort(404)
        
        # Traduz classificação indicativa para padrão brasileiro
        if jogo.get('esrb_rating') and jogo['esrb_rating'].get('name'):
            classificacao_esrb = jogo['esrb_rating']['name']
            jogo['classificacao_br'] = CLASSIFICACAO_TRADUCAO.get(classificacao_esrb, 'N/A')
        else:
            jogo['classificacao_br'] = 'N/A'
        
        # Traduz e monta string de gêneros
        generos_lista = jogo.get('genres', [])
        if generos_lista:
            generos_traduzidos = [GENEROS_TRADUCAO.get(g['name'], g['name']) for g in generos_lista]
            generos = ', '.join(generos_traduzidos)
        else:
            generos = 'N/A'
        
        # Processa plataformas 
        plataformas_lista = jogo.get('platforms', [])
        if plataformas_lista:
            plataformas = ', '.join([p['platform']['name'] for p in plataformas_lista[:4]])
        else:
            plataformas = 'N/A'
        
        # Limpa sinopse do jogo
        descricao_raw = jogo.get('description_raw', '')
        if descricao_raw:
            descricao_limpa = descricao_raw.split('###')[0].split('\n\n')[0].strip()
            jogo['description_clean'] = descricao_limpa
        else:
            jogo['description_clean'] = 'Descrição não disponível.'
        
        trailer_url = None
        
        # 1. Tenta usar o trailer do RAWG
        if jogo.get('clip') and jogo['clip'].get('clip'):
            trailer_url = jogo['clip']['clip']
            print(f"Usando trailer do RAWG")
        else:
            # 2. Se não houver, busca trailer na Steam
            print(f"RAWG sem trailer. Buscando na Steam...")
            trailer_url = obter_trailer_steam(jogo.get('name'))
        
        jogo['trailer_url'] = trailer_url
        
        return render_template('detalhes_jogos.html',
                             jogo=jogo,
                             generos=generos,
                             plataformas=plataformas)
    
    except Exception as e:
        print(f"Erro ao buscar detalhes do jogo: {e}")
        import traceback
        traceback.print_exc()
        abort(500)