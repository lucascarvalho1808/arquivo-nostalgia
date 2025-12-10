import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAWG_API_KEY = os.environ.get('RAWG_API_KEY')
BASE_URL = "https://api.rawg.io/api"

def _formatar_jogos(resultados):
    """
    Padroniza os dados dos jogos para ficarem parecidos com os de filmes.
    """
    jogos_formatados = []
    for jogo in resultados:
        jogos_formatados.append({
            'id': jogo['id'],
            'titulo': jogo['name'],
            'sinopse': "Sinopse disponível nos detalhes.", 
            'data_lancamento': jogo.get('released'),
            'poster_url': jogo.get('background_image'), 
            'nota': jogo.get('rating'), # Nota de 0 a 5
            'plataformas': [p['platform']['name'] for p in jogo.get('platforms', [])], # Lista de plataformas 
            'tipo': 'game'
        })
    return jogos_formatados

def buscar_jogos_populares(pagina=1, page_size=20):
    """
    Busca jogos populares (ordenados por 'added', ou seja, mais adicionados às bibliotecas).
    """
    endpoint = f"{BASE_URL}/games"
    
    params = {
        'key': RAWG_API_KEY,
        'page': pagina,
        'page_size': page_size,
        'ordering': '-added' # Ordena pelos mais populares
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        dados = response.json()
        return _formatar_jogos(dados.get('results', []))

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com a API da RAWG: {e}")
        return []

def pesquisar_jogos(query, pagina=1):
    """
    Pesquisa jogos pelo nome.
    """
    endpoint = f"{BASE_URL}/games"
    
    params = {
        'key': RAWG_API_KEY,
        'page': pagina,
        'search': query, # Parâmetro de busca da RAWG
        'ordering': '-added' # Traz os mais populares primeiro na busca
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_jogos(response.json().get('results', []))
    except requests.exceptions.RequestException as e:
        print(f"Erro ao pesquisar jogo '{query}': {e}")
        return []

def buscar_detalhes_jogo(jogo_id):
    """
    Busca os detalhes completos de um jogo específico pelo ID.
    """
    endpoint = f"{BASE_URL}/games/{jogo_id}"
    params = {
        'key': RAWG_API_KEY
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        jogo = response.json()

        # Remove tags HTML da descrição (a RAWG retorna <p>texto</p>)
        import re
        descricao_limpa = re.sub('<[^<]+?>', '', jogo.get('description', ''))

        return {
            'id': jogo['id'],
            'titulo': jogo['name'],
            'sinopse': descricao_limpa or "Descrição indisponível.",
            'data_lancamento': jogo.get('released'),
            'poster_url': jogo.get('background_image'),
            'nota': jogo.get('rating'),
            'generos': [g['name'] for g in jogo.get('genres', [])],
            'plataformas': [p['platform']['name'] for p in jogo.get('platforms', [])],
            'desenvolvedores': [d['name'] for d in jogo.get('developers', [])],
            'website': jogo.get('website'),
            'tipo': 'game'
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar detalhes do jogo {jogo_id}: {e}")
        return None

# Teste 
if __name__ == "__main__":
    print("--- Testando Jogos Populares ---")
    jogos = buscar_jogos_populares()
    if jogos:
        print(f"Jogo mais popular: {jogos[0]['titulo']} (Nota: {jogos[0]['nota']})")
        print(f"Imagem: {jogos[0]['poster_url']}")
    else:
        print("Nenhum jogo encontrado.")

    print("\n--- Testando Pesquisa (Mario) ---")
    busca = pesquisar_jogos("Mario")
    if busca:
        print(f"Primeiro resultado: {busca[0]['titulo']}")