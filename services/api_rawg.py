import os
import requests
import re
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

def _extrair_steam_id(stores):
    """
    Tenta encontrar o ID da Steam dentro da lista de lojas da RAWG.
    """
    if not stores:
        return None
        
    for loja_item in stores:
        store_info = loja_item.get('store', {})
        if store_info.get('slug') == 'steam':
            url_loja = loja_item.get('url', '')
            match = re.search(r'/app/(\d+)', url_loja)
            if match:
                return match.group(1)
    return None

def _buscar_dados_steam(app_id):
    """
    Busca dados ricos (Preço, PT-BR, Requisitos) na API pública da Steam.
    """
    url_steam = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=brazilian"
    try:
        response = requests.get(url_steam, timeout=5)
        dados = response.json()
        
        # Verifica se a requisição foi bem sucedida na estrutura da Steam
        if dados and str(app_id) in dados and dados[str(app_id)]['success']:
            return dados[str(app_id)]['data']
    except Exception as e:
        print(f"Erro ao conectar na Steam: {e}")
    
    return None

def _formatar_jogo_hibrido(dados_rawg, dados_steam=None):
    """
    Mescla os dados. Prioriza Steam para texto/preço e RAWG para metadados.
    """
    jogo = {
        'id': dados_rawg.get('id'),
        'titulo': dados_rawg.get('name'),
        'poster_url': dados_rawg.get('background_image'), # RAWG costuma ter imagens melhores/maiores
        'lancamento': dados_rawg.get('released'),
        'nota': dados_rawg.get('metacritic'),
        'generos': [g['name'] for g in dados_rawg.get('genres', [])],
        'plataformas': [p['platform']['name'] for p in dados_rawg.get('platforms', [])],
        
        # Dados que tentaremos pegar da Steam (padrão RAWG ou vazio se falhar)
        'descricao': dados_rawg.get('description_raw', ''),
        'preco': 'Não informado',
        'requisitos': None,
        'loja_url': f"https://rawg.io/games/{dados_rawg.get('slug')}"
    }

    # Se tivermos dados da Steam, enriquecemos o objeto
    if dados_steam:
        # Descrição em Português
        if 'short_description' in dados_steam:
            jogo['descricao'] = dados_steam['short_description']
        
        # Preço em Reais
        if 'price_overview' in dados_steam:
            jogo['preco'] = dados_steam['price_overview'].get('final_formatted', 'Grátis')
        elif dados_steam.get('is_free'):
            jogo['preco'] = 'Gratuito'

        # Requisitos de Sistema (PC)
        if 'pc_requirements' in dados_steam and 'minimum' in dados_steam['pc_requirements']:
            jogo['requisitos'] = dados_steam['pc_requirements']['minimum']
            
        # Imagem de Capa (Opcional: Steam Header às vezes é melhor para cards horizontais)
        # jogo['poster_url'] = dados_steam.get('header_image', jogo['poster_url'])

    return jogo

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