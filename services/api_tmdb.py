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
    endpoint = f"{BASE_URL}/search/multi" # 'multi' busca filmes e séries ao mesmo tempo
    params = {
        'api_key': TMDB_API_KEY, 
        'language': 'pt-BR', 
        'page': pagina,
        'query': query,
        'include_adult': 'flase' 
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_resultados(response.json().get('results', []))
    except requests.exceptions.RequestException as e:
        print(f"Erro ao pesquisar mídia '{query}': {e}")
        return []

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