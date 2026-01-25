import os
import requests
import re
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Chave da API RAWG e URL base
RAWG_API_KEY = os.environ.get('RAWG_API_KEY')
BASE_URL = "https://api.rawg.io/api"

# Cache para IDs da Steam já buscados
_steam_id_cache = {}

def _buscar_id_steam_por_nome(nome_jogo):
    """
    Busca o AppID da Steam usando o nome do jogo na API de busca da Steam.
    Usa cache para evitar requisições repetidas.
    """
    if nome_jogo in _steam_id_cache:
        return _steam_id_cache[nome_jogo]

    try:
        url = f"https://store.steampowered.com/api/storesearch/?term={nome_jogo}&l=english&cc=US"
        response = requests.get(url, timeout=1)
        data = response.json()
        
        if data and data.get('total') > 0:
            items = data.get('items', [])
            if items:
                steam_id = str(items[0]['id'])
                _steam_id_cache[nome_jogo] = steam_id
                return steam_id
    except:
        pass
    
    return None

def _extrair_steam_id(stores, nome_jogo):
    """
    Tenta encontrar o ID da Steam para o jogo.
    1. Tenta pela URL da RAWG (se disponível).
    2. Se tiver loja Steam mas sem URL, busca pelo nome na Steam.
    """
    tem_steam = False
    
    if stores:
        for loja_item in stores:
            store_info = loja_item.get('store', {})
            if store_info.get('slug') == 'steam':
                tem_steam = True
                url_loja = loja_item.get('url', '') or loja_item.get('url_en', '')
                match = re.search(r'/app/(\d+)', str(url_loja))
                if match:
                    return match.group(1)
                break
    
    if tem_steam and nome_jogo:
        return _buscar_id_steam_por_nome(nome_jogo)
        
    return None

def _gerar_capa_steam(steam_id):
    """
    Gera a URL da capa vertical da Steam.
    """
    if not steam_id:
        return None
    return f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{steam_id}/library_600x900.jpg"

def _buscar_dados_steam_detalhes(app_id):
    """
    Busca dados ricos na API pública da Steam para um app_id.
    """
    url_steam = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=brazilian"
    try:
        response = requests.get(url_steam, timeout=3)
        dados = response.json()
        if dados and str(app_id) in dados and dados[str(app_id)]['success']:
            return dados[str(app_id)]['data']
    except Exception as e:
        print(f"Erro ao conectar na Steam: {e}")
    return None

def _formatar_jogos_lista(resultados):
    """
    Formata a lista de jogos retornada pela RAWG.
    Define se usa estilo Steam (capa vertical) ou RAWG (imagem padrão).
    """
    jogos_formatados = []
    for jogo in resultados:
        steam_id = _extrair_steam_id(jogo.get('stores', []), jogo.get('name'))
        capa_steam = _gerar_capa_steam(steam_id)
        
        if capa_steam:
            poster_principal = capa_steam
            origem = 'steam'
        else:
            poster_principal = jogo.get('background_image')
            origem = 'rawg'

        jogos_formatados.append({
            'id': jogo['id'],
            'titulo': jogo['name'],
            'slug': jogo.get('slug'),
            'poster_url': poster_principal,
            'imagem_rawg': jogo.get('background_image'), 
            'origem_imagem': origem,
            'nota': jogo.get('metacritic'),
            'tipo': 'game'
        })
    return jogos_formatados

def buscar_jogos_populares(pagina=1, page_size=25):
    """
    Busca jogos populares na RAWG.
    """
    endpoint = f"{BASE_URL}/games"
    params = {
        'key': RAWG_API_KEY,
        'ordering': '-added',
        'page_size': page_size,
        'page': pagina
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_jogos_lista(response.json().get('results', []))

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar jogos na RAWG: {e}")
        return []

def pesquisar_jogos(query):
    """
    Pesquisa jogos por nome na RAWG.
    """
    endpoint = f"{BASE_URL}/games"
    params = {
        'key': RAWG_API_KEY,
        'search': query,
        'page_size': 12
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return _formatar_jogos_lista(response.json().get('results', []))

    except requests.exceptions.RequestException as e:
        print(f"Erro ao pesquisar jogos: {e}")
        return []

def buscar_detalhes_jogo(jogo_id):
    """
    Busca detalhes completos de um jogo específico no RAWG.
    
    Args:
        jogo_id (int): ID do jogo no RAWG
    
    Returns:
        dict: Dados completos do jogo incluindo screenshots
    """
    try:
        # Busca dados principais do jogo
        url = f"{BASE_URL}/games/{jogo_id}"
        params = {
            'key': RAWG_API_KEY
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        jogo = response.json()
        
        # Busca screenshots separadamente
        screenshots_url = f"{BASE_URL}/games/{jogo_id}/screenshots"
        screenshots_response = requests.get(screenshots_url, params=params)
        
        if screenshots_response.status_code == 200:
            screenshots_data = screenshots_response.json()
            jogo['screenshots'] = screenshots_data.get('results', [])
            print(f"Screenshots encontrados: {len(jogo['screenshots'])}")
        else:
            jogo['screenshots'] = []
            print("Nenhum screenshot encontrado")
        
        # DEBUG
        print(f"\n=== DEBUG JOGO {jogo_id} ===")
        print(f"Nome: {jogo.get('name')}")
        print(f"Clip disponível: {jogo.get('clip')}")
        print(f"Screenshots carregados: {len(jogo.get('screenshots', []))}")
        if jogo.get('screenshots'):
            print(f"Primeiro screenshot: {jogo['screenshots'][0].get('image')}")
        print(f"=========================\n")
        
        return jogo
    
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Jogo com ID {jogo_id} não encontrado.")
        else:
            print(f"Erro HTTP ao buscar jogo {jogo_id}: {http_err}")
        return None
    
    except Exception as e:
        print(f"Erro ao buscar detalhes do jogo {jogo_id}: {e}")
        import traceback
        traceback.print_exc()
        return None

def buscar_catalogo_jogos(pagina=1):
    """
    Busca jogos para a página /jogos.
    Usa a mesma lógica de formatação da Home.
    """
    endpoint = f"{BASE_URL}/games"
    params = {
        'key': RAWG_API_KEY,
        'page': pagina,
        'page_size': 20,
        'ordering': '-added',
    }
    
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        resultados = response.json().get('results', [])
        
        # Usa a mesma função de formatação da Home
        jogos = _formatar_jogos_lista(resultados)
        
        # Adiciona campos extras para a página de catálogo
        for jogo in jogos:
            jogo['imagem_fallback'] = jogo.get('imagem_rawg')
            jogo['data_lancamento'] = None
        
        return jogos

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar catálogo de jogos: {e}")
        return []

def buscar_jogos_por_genero(generos, pagina=1):
    """
    Busca jogos filtrados por gênero.
    Usa a mesma lógica de formatação da Home.
    """
    endpoint = f"{BASE_URL}/games"
    params = {
        'key': RAWG_API_KEY,
        'page': pagina,
        'page_size': 20,
        'ordering': '-added',
        'genres': generos
    }
    
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        resultados = response.json().get('results', [])
        
        # Usa a mesma função de formatação da Home
        jogos = _formatar_jogos_lista(resultados)
        
        # Adiciona campos extras para a página de catálogo
        for jogo in jogos:
            jogo['imagem_fallback'] = jogo.get('imagem_rawg')
            jogo['data_lancamento'] = None
        
        return jogos

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar jogos por gênero: {e}")
        return []

def buscar_jogos(termo, max_resultados=200):
    """
    Busca jogos pelo termo digitado com múltiplas páginas (até 200 resultados).
    """
    try:
        jogos = []
        pagina = 1
        page_size = 20
        
        while len(jogos) < max_resultados:
            url = f"{BASE_URL}/games"
            params = {
                "key": RAWG_API_KEY,
                "search": termo,
                "page": pagina,
                "page_size": page_size
            }
            
            response = requests.get(url, params=params, timeout=5)
            dados = response.json()
            
            resultados_pagina = dados.get("results", [])
            
            # Se não há mais resultados, para o loop
            if not resultados_pagina:
                break
            
            for jogo in resultados_pagina:
                if len(jogos) >= max_resultados:
                    break
                    
                jogos.append({
                    "id": jogo.get("id"),
                    "titulo": jogo.get("name"),
                    "poster": jogo.get("background_image"),
                    "ano": jogo.get("released", "")[:4] if jogo.get("released") else "",
                    "nota": jogo.get("rating"),
                    "tipo": "jogo"
                })
            
            # Se chegou ao limite, para
            if len(jogos) >= max_resultados:
                break
            
            # Se retornou menos que page_size, não há mais páginas
            if len(resultados_pagina) < page_size:
                break
                
            pagina += 1
        
        return jogos
        
    except Exception as e:
        print(f"Erro ao buscar jogos: {e}")
        return []

# Testes
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