import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def _formatar_resultados(resultados, tipo_midia_padrao=None):
    """
    Função auxiliar para formatar a lista de resultados (filmes ou séries)
    de maneira padronizada para o nosso HTML.
    """
    lista_formatada = []
    for item in resultados:
        # O TMDB retorna 'title' para filmes e 'name' para séries
        titulo = item.get('title') or item.get('name')
        
        # Data de lançamento também 
        data = item.get('release_date') or item.get('first_air_date')
        
        # Define o tipo 
        tipo = item.get('media_type') or tipo_midia_padrao

        if titulo: # Só adiciona se tiver título
            lista_formatada.append({
                'id': item['id'],
                'titulo': titulo,
                'sinopse': item.get('overview', 'Sinopse indisponível.'),
                'data_lancamento': data,
                'poster_url': f"{IMAGE_BASE_URL}{item['poster_path']}" if item.get('poster_path') else None,
                'nota': item.get('vote_average'),
                'tipo': tipo # Útil para saber se é filme ou série no link de detalhes
            })
    return lista_formatada

def buscar_filmes_populares(pagina=1):
    """
    Busca os filmes populares atuais no TMDB.
    Retorna uma lista de dicionários com os dados dos filmes.
    """
    endpoint = f"{BASE_URL}/movie/popular"
    
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'pt-BR', # Traz os resultados em português
        'page': pagina
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status() # Levanta erro se a requisição falhar
        
        dados = response.json()
        filmes = dados.get('results', [])

        # Processa os dados para facilitar o uso no HTML
        filmes_formatados = []
        for filme in filmes:
            filmes_formatados.append({
                'id': filme['id'],
                'titulo': filme['title'],
                'sinopse': filme['overview'],
                'data_lancamento': filme['release_date'],
                # Monta a URL completa da imagem. Se não tiver imagem, pode colocar uma padrão depois.
                'poster_url': f"{IMAGE_BASE_URL}{filme['poster_path']}" if filme.get('poster_path') else None,
                'nota': filme['vote_average']
            })
            
        return filmes_formatados

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com a API do TMDB: {e}")
        return []

def buscar_series_populares(pagina=1):
    """
    Busca as séries populares atuais no TMDB.
    Retorna uma lista de dicionários com os dados das séries.
    """
    endpoint = f"{BASE_URL}/tv/popular"
    params = {'api_key': TMDB_API_KEY, 'language': 'pt-BR', 'page': pagina}
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_resultados(response.json().get('results', []), tipo_midia_padrao='tv')
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar séries: {e}")
        return []

def pesquisar_midia(query, pagina=1):
    """
    Pesquisa por filmes e séries com base em um texto (query).
    """
    endpoint = f"{BASE_URL}/search/multi" 
    params = {
        'api_key': TMDB_API_KEY, 
        'language': 'pt-BR', 
        'page': pagina,
        'query': query,
        'include_adult': 'false'
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_resultados(response.json().get('results', []))
    except requests.exceptions.RequestException as e:
        print(f"Erro ao pesquisar mídia '{query}': {e}")
        return []

def buscar_detalhes_filme(filme_id):
    """
    Busca detalhes completos de um filme específico no TMDB.
    
    Args:
        filme_id (int): ID do filme no TMDB
    
    Returns:
        dict: Dados completos do filme incluindo credits e videos
    """
    try:
        url = f"{BASE_URL}/movie/{filme_id}"
        params = {
            'api_key': TMDB_API_KEY,  
            'language': 'pt-BR',
            'append_to_response': 'credits,videos,release_dates' 
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Filme com ID {filme_id} não encontrado.")
        else:
            print(f"Erro HTTP ao buscar filme {filme_id}: {http_err}")
        return None
    
    except Exception as e:
        print(f"Erro ao buscar detalhes do filme {filme_id}: {e}")
        return None

def buscar_filmes_classicos(pagina=[1, 2]):
    """
    Busca filmes bem avaliados (Top Rated) para a seção de Clássicos.
    """
    endpoint = f"{BASE_URL}/movie/top_rated"
    
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'pt-BR',
        'page': pagina
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_resultados(response.json().get('results', []), tipo_midia_padrao='movie')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar filmes clássicos: {e}")
        return []

def buscar_series_nostalgia(pagina=1):
    """
    Busca séries populares que foram lançadas antes de 2010 (Anos 2000/90).
    """
    endpoint = f"{BASE_URL}/discover/tv"
    
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'pt-BR',
        'sort_by': 'vote_count.desc', 
        'first_air_date.lte': '2014-12-31', # Apenas séries lançadas antes de 2014
        'first_air_date.gte': '1990-01-01', # A partir de 1990
        'page': pagina
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_resultados(response.json().get('results', []), tipo_midia_padrao='tv')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar séries nostalgia: {e}")
        return []

def buscar_catalogo_filmes(pagina=1):
    """
    Função para a página /filmes.
    Busca filmes populares para preencher a grade do catálogo.
    Usa a função auxiliar _formatar_resultados para garantir os campos corretos.
    """
    endpoint = f"{BASE_URL}/movie/popular"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'pt-BR',
        'page': pagina
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        # Reutiliza a formatação padrão para garantir que tenha 'poster_url', 'titulo', etc.
        return _formatar_resultados(response.json().get('results', []), tipo_midia_padrao='movie')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar catálogo de filmes: {e}")
        return []

def buscar_catalogo_series(pagina=1):
    """
    Função para a página /series.
    Busca séries populares para preencher a grade do catálogo.
    """
    endpoint = f"{BASE_URL}/tv/popular"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'pt-BR',
        'page': pagina
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_resultados(response.json().get('results', []), tipo_midia_padrao='tv')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar catálogo de séries: {e}")
        return []

def buscar_filmes_por_genero(generos, pagina=1):
    """
    Busca filmes filtrados por gênero(s).
    
    Args:
        generos: String com IDs separados por vírgula (ex: "28,12,35")
        pagina: Número da página
    
    Returns:
        Lista de filmes formatados
    """
    endpoint = f"{BASE_URL}/discover/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'pt-BR',
        'page': pagina,
        'sort_by': 'popularity.desc',
        'with_genres': generos 
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_resultados(response.json().get('results', []), tipo_midia_padrao='movie')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar filmes por gênero: {e}")
        return []

def buscar_series_por_genero(generos, pagina=1):
    """
    Busca séries filtradas por gênero(s).
    
    Args:
        generos: String com IDs separados por vírgula (ex: "16,35,18")
        pagina: Número da página
    
    Returns:
        Lista de séries formatadas
    """
    endpoint = f"{BASE_URL}/discover/tv"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'pt-BR',
        'page': pagina,
        'sort_by': 'popularity.desc',
        'with_genres': generos
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_resultados(response.json().get('results', []), tipo_midia_padrao='tv')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar séries por gênero: {e}")
        return []

def buscar_filmes(termo, max_resultados=200):
    """Busca filmes pelo termo digitado com múltiplas páginas (até 200 resultados)"""
    try:
        filmes = []
        pagina = 1
        
        while len(filmes) < max_resultados:
            url = f"{BASE_URL}/search/movie"
            params = {
                "api_key": TMDB_API_KEY,
                "language": "pt-BR",
                "query": termo,
                "page": pagina
            }
            
            response = requests.get(url, params=params, timeout=5)
            dados = response.json()
            
            resultados_pagina = dados.get("results", [])
            
            # Se não há mais resultados, para o loop
            if not resultados_pagina:
                break
            
            for filme in resultados_pagina:
                if len(filmes) >= max_resultados:
                    break
                    
                filmes.append({
                    "id": filme.get("id"),
                    "titulo": filme.get("title"),
                    "poster": f"https://image.tmdb.org/t/p/w300{filme.get('poster_path')}" if filme.get("poster_path") else None,
                    "ano": filme.get("release_date", "")[:4] if filme.get("release_date") else "",
                    "nota": filme.get("vote_average"),
                    "tipo": "filme"
                })
            
            # Se chegou ao limite, para
            if len(filmes) >= max_resultados:
                break
            
            # Se retornou menos que 20, não há mais páginas
            if len(resultados_pagina) < 20:
                break
            
            # TMDB tem limite de 500 páginas
            if pagina >= 500:
                break
                
            pagina += 1
        
        return filmes
        
    except Exception as e:
        print(f"Erro ao buscar filmes: {e}")
        return []


def buscar_series(termo, max_resultados=200):
    """Busca séries pelo termo digitado com múltiplas páginas (até 200 resultados)"""
    try:
        series = []
        pagina = 1
        
        while len(series) < max_resultados:
            url = f"{BASE_URL}/search/tv"
            params = {
                "api_key": TMDB_API_KEY,
                "language": "pt-BR",
                "query": termo,
                "page": pagina
            }
            
            response = requests.get(url, params=params, timeout=5)
            dados = response.json()
            
            resultados_pagina = dados.get("results", [])
            
            # Se não há mais resultados, para o loop
            if not resultados_pagina:
                break
            
            for serie in resultados_pagina:
                if len(series) >= max_resultados:
                    break
                    
                series.append({
                    "id": serie.get("id"),
                    "titulo": serie.get("name"),
                    "poster": f"https://image.tmdb.org/t/p/w300{serie.get('poster_path')}" if serie.get("poster_path") else None,
                    "ano": serie.get("first_air_date", "")[:4] if serie.get("first_air_date") else "",
                    "nota": serie.get("vote_average"),
                    "tipo": "serie"
                })
            
            # Se chegou ao limite, para
            if len(series) >= max_resultados:
                break
            
            # Se retornou menos que 20, não há mais páginas
            if len(resultados_pagina) < 20:
                break
            
            # TMDB tem limite de 500 páginas
            if pagina >= 500:
                break
                
            pagina += 1
        
        return series
        
    except Exception as e:
        print(f"Erro ao buscar séries: {e}")
        return []

def buscar_detalhes_serie(serie_id):
    """
    Busca detalhes completos de uma série específica no TMDB.
    
    Args:
        serie_id (int): ID da série no TMDB
    
    Returns:
        dict: Dados completos da série incluindo credits e videos
    """
    try:
        url = f"{BASE_URL}/tv/{serie_id}"
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'pt-BR',
            'append_to_response': 'credits,videos,content_ratings'  
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Série com ID {serie_id} não encontrada.")
        else:
            print(f"Erro HTTP ao buscar série {serie_id}: {http_err}")
        return None
    
    except Exception as e:
        print(f"Erro ao buscar detalhes da série {serie_id}: {e}")
        return None

# Teste rápido das funções
if __name__ == "__main__":
    print("--- Testando Filmes ---")
    filmes = buscar_filmes_populares()
    print(f"Filme popular: {filmes[0]['titulo'] if filmes else 'Nenhum'}")

    print("\n--- Testando Séries ---")
    series = buscar_series_populares()
    print(f"Série popular: {series[0]['titulo'] if series else 'Nenhuma'}")

    print("\n--- Testando Pesquisa (Batman) ---")
    busca = pesquisar_midia("Batman")
    print(f"Resultados encontrados: {len(busca)}")
    if busca:
        print(f"Primeiro resultado: {busca[0]['titulo']} ({busca[0]['tipo']})")