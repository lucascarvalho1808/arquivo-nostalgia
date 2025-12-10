import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500" # URL base para carregar imagens (posters)

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

# Teste da função
if __name__ == "__main__":
    print("Testando busca de filmes populares...")
    resultados = buscar_filmes_populares()
    if resultados:
        print(f"Sucesso! Encontrados {len(resultados)} filmes.")
        print(f"Primeiro filme: {resultados[0]['titulo']}")
    else:
        print("Falha ao buscar filmes.")